from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from llm_service import chat_with_glm
from fastapi.middleware.cors import CORSMiddleware
from db_manager import LegalDB
import pandas as pd
import os
import uvicorn
import csv
from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain_chroma import Chroma
from langchain_core.documents import Document

app = FastAPI(title="法律咨询聊天机器人")

# 允许前端跨域
app.add_middleware(
    CORSMiddleware, 
    allow_origins=["*"], 
    allow_methods=["*"], 
    allow_headers=["*"]
)

# RAG 核心参数配置
MODEL_NAME = "qwen2.5:1.5b" 
VECTOR_DB_PATH = "./vector_db"

print(f"正在初始化本地模型: {MODEL_NAME}...")
try:
    # 统一 Embedding 和 LLM 模型，减少显存碎片
    embeddings = OllamaEmbeddings(model=MODEL_NAME)
    local_llm = OllamaLLM(
        model=MODEL_NAME, 
        temperature=0.1,
        num_ctx=2048
    )
except Exception as e:
    print(f"本地模型初始化失败: {e}")

# 向量库
def init_vector_db():
    if os.path.exists(VECTOR_DB_PATH):
        print("加载现有向量库...")
        return Chroma(persist_directory=VECTOR_DB_PATH, embedding_function=embeddings)
    
    print("正在读取 laws_structured.csv 并构建向量库...")
    texts = []
    try:
        if os.path.exists("laws_structured.csv"):
            with open("laws_structured.csv", "r", encoding="utf-8", errors="ignore") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if "text" in row and row["text"].strip():
                        texts.append(row["text"].strip())
        
        if not texts:
            texts = ["试用期提前3天可离职", "公司应按月发放工资"]
            
        docs = [Document(page_content=t) for t in texts]
        vs = Chroma.from_documents(
            documents=docs,
            embedding=embeddings,
            persist_directory=VECTOR_DB_PATH
        )
        print("向量库构建完成")
        return vs
    except Exception as e:
        print(f"向量库构建失败: {e}")
        return None

vector_store = init_vector_db()
retriever = vector_store.as_retriever(search_kwargs={"k": 3}) if vector_store else None

# 数据库实例
db = LegalDB()

class ChatRequest(BaseModel):
    question: str
    category: str = "general"
    user_id: str = "test_user_01"
    model_type: str = "api"

# 核心接口

@app.get("/")
def health_check():
    return {"status": "online", "model": MODEL_NAME}

@app.post("/api/chat/send")
async def chat_send(req: ChatRequest):
    # 预设响应结构，防止前端 undefined
    response_data = {
        "code": 200,
        "answer": "抱歉，服务器暂时无法处理您的请求。",
        "mode": req.model_type
    }

    try:
        # 获取历史上下文
        history_data = db.get_history(req.user_id, req.category)
        formatted_history = [{"role": r['role'], "content": r['content']} for r in history_data]

        if req.model_type == "local_rag":
            if not retriever:
                response_data["answer"] = "本地检索服务未启动，请检查数据集。"
            else:
                # 执行 RAG 流程
                docs = retriever.invoke(req.question)
                context = "\n".join([d.page_content for d in docs])
                prompt = f"参考法条：\n{context}\n\n问题：{req.question}\n请简要回答："
                
                print(f"正在进行本地推理: {req.question}")
                try:
                    raw_res = local_llm.invoke(prompt)
                    response_data["answer"] = str(raw_res) if raw_res else "本地模型未生成内容。"
                except Exception as model_e:
                    print(f"本地模型运行崩溃: {model_e}")
                    response_data["answer"] = "本地显存不足，请清理后台程序或切换到 API 模式。"
        else:
            # API 模式
            response_data["answer"] = chat_with_glm(req.question, formatted_history)

        # 确保存储到数据库的内容不为空
        final_answer = response_data["answer"]
        db.save_chat_log(req.user_id, req.category, 'user', req.question)
        db.save_chat_log(req.user_id, req.category, 'assistant', final_answer)

        return response_data

    except Exception as e:
        print(f"全局服务器错误: {e}")
        return {"code": 500, "answer": f"后端异常: {str(e)}", "mode": req.model_type}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5000)