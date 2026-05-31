from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
import os

# 1. 启动后端
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. 读取法律文件 → 构建本地向量库（已按你的CSV列名修改）
def build_vector_db():
    # 读取CSV文件，指定UTF-8编码避免乱码
    df = pd.read_csv("laws_structured.csv", encoding="utf-8")

    # 把法条转成文档格式（这里改成了你文件里的列名text）
    docs = []
    for _, row in df.iterrows():
        content = f"法律条文：{row['text']}"
        docs.append(Document(page_content=content))

    # 初始化向量模型
    embeddings = OllamaEmbeddings(model="qwen3:8b-q4_K_M")

    # 生成并持久化向量库
    db = Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        persist_directory="./vector_db"
    )
    db.persist()
    return db

# 启动时自动加载向量库
if not os.path.exists("./vector_db"):
    print("正在构建法律向量库，首次运行可能较慢...")
    db = build_vector_db()
else:
    print("加载已存在的向量库...")
    embeddings = OllamaEmbeddings(model="qwen3:8b-q4_K_M")
    db = Chroma(persist_directory="./vector_db", embedding_function=embeddings)

retriever = db.as_retriever(search_kwargs={"k": 3})

# 3. 初始化本地模型
llm = OllamaLLM(model="qwen3:8b-q4_K_M", temperature=0.1)

# 4. 核心RAG问答接口
class Question(BaseModel):
    question: str

@app.post("/api/chat")
def chat(req: Question):
    # 步骤1：从向量库检索相关法条
    docs = retriever.invoke(req.question)
    context = "\n".join([d.page_content for d in docs])

    # 步骤2：给模型的提示词，限定它用法条回答
    prompt = f"""你是专业的法律咨询助手，请严格根据下面提供的法律条文回答用户问题，不要编造法条。

参考法条：
{context}

用户问题：{req.question}
"""

    # 步骤3：调用模型生成回答
    answer = llm.invoke(prompt)

    # 返回结果，包含引用的法条
    return {
        "code": 200,
        "question": req.question,
        "answer": answer,
        "referenced_laws": context
    }

# 测试接口
@app.get("/")
def home():
    return {"status": "✅ 本地RAG向量库后端运行成功！"}