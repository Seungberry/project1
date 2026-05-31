from fastapi import FastAPI
from pydantic import BaseModel
from llm_service import chat_with_glm
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="法律AI后端")

# 允许前端跨域（必须加，否则前端联调失败）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 接口参数格式
class ChatRequest(BaseModel):
    question: str
    conversation_id: str = ""

# 核心对话接口
@app.post("/api/chat/send")
def chat(req: ChatRequest):
    answer = chat_with_glm(req.question)
    return {
        "code": 200,
        "question": req.question,
        "answer": answer
    }

# 测试接口
@app.get("/")
def index():
    return {"message": "法律AI后端运行成功！"}