# 基于 RAG 架构与混合模型的智能法律咨询系统

[![FastAPI](https://img.shields.io/badge/FastAPI-0055FF?style=flat&logo=FastAPI&logoColor=white)](https://fastapi.tiangolo.com/)
[![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?style=flat)](https://github.com/langchain-ai/langchain)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-E4405F?style=flat)](https://github.com/chroma-core/chroma)
[![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=flat&logo=MySQL&logoColor=white)](https://www.mysql.com/)

一个全栈架构的智能法律咨询聊天机器人系统。系统支持本地 RAG（检索增强生成）知识库模式与云端大模型 API 模式的动态双驱动切换。具备数据深度清洗、法律场景分类、多轮对话记忆持久化以及 Web 可视化交互等核心能力。

## 核心特性

- **双模式智能分发**：
  - 本地 RAG 模式：基于 Chroma向量数据库与本地 Ollama (Qwen2.5) 嵌入及推理模型，严格依据本地结构化法条回答，有效杜绝大模型“幻觉”。
  - API 模式：直连高性能云端 智谱 GLM-4-Flash 模型，处理复杂法理逻辑推演。
- **上下文多轮对话持久化**：采用 FastAPI 异步接口调度，结合 MySQL 数据库自动存取历史日志，建立具备记忆能力的连续对话流。
- **全链路工程闭环**：
  - 数据端：提供高效的数据清洗与标准化处理脚本 (lawsAI.ipynb)。
  - 前端：响应式原生 Web 交互界面，支持场景卡片引导与流式交互感。
  - 测试端：内置多线程高并发压力测试与性能可视化分析工具。
<img width="1408" height="768" alt="项目" src="https://github.com/user-attachments/assets/7429f6c2-5df7-452e-9560-e39f89446f4c" />

---

## 项目文件结构

```text
├── laws_structured.csv     # 经过结构化清洗的法律法规数据集
├── lawsAI.ipynb            # 法律大数据清洗、去重与标准化 Jupyter 笔记本
├── main.py                 # FastAPI 后端核心业务调度与路由网关
├── db_manager.py           # MySQL 数据库交互模块（对话日志存储与上下文读取）
├── llm_service.py          # 智谱 GLM API 对话服务适配器
├── index.html              # 前端交互 Web 界面
├── test.py                 # 多线程高并发压力测试脚本
├── visual.py               # 压测性能分析与吞吐量可视化绘图脚本
├── qwen.py / GLM.py        # 基础大模型多轮对话测试（终端版）
└── rag_chat.py             # 独立 RAG 问答链功能原型测试脚本

```

---

## 环境搭建与运行指南

### 1. 依赖安装

确保你的系统已安装 Python 3.9+。

```bash

pip install fastapi==0.115.12 uvicorn==0.34.0 -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install langchain-ollama langchain-chroma -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install pymysql openai -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install pandas requests matplotlib -i https://pypi.tuna.tsinghua.edu.cn/simple
```

> **主要依赖项**：`fastapi`, `uvicorn`, `langchain-ollama`, `langchain-chroma`, `pymysql`, `openai`, `pandas`, `requests`, `matplotlib`

### 2. 部署本地大模型环境

1. 下载并安装 [Ollama](https://ollama.com/)。
2. 在终端拉取优化版的 Qwen 模型（推荐 1.5B/3B 版本以平衡推理速度与显存）：
```bash
ollama pull qwen2.5:1.5b
```



### 3. 初始化 MySQL 数据库

在本地 MySQL 中创建名为 `legal_bot_db` 的数据库，并建立以下日志表：

```sql
CREATE DATABASE IF NOT EXISTS legal_bot_db CHARSET utf8mb4;
USE legal_bot_db;

CREATE TABLE IF NOT EXISTS chat_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL,
    category VARCHAR(20) NOT NULL,
    role VARCHAR(20) NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

```

> *注：如需修改数据库账户密码，请前往 `db_manager.py` 进行配置。*
<img width="1918" height="1013" alt="屏幕截图 2026-05-09 083601" src="https://github.com/user-attachments/assets/f4fd7a30-50cf-42ff-96f6-c7684c7931f9" />

### 4. 启动系统

**第一步：启动后端服务**

```bash
python main.py

```

系统启动时会自动检测本地是否已有 `vector_db` 向量库，若没有则会自动读取 `laws_structured.csv` 并通过大模型 Embedding 建立向量库。服务默认运行在 `http://127.0.0.1:5000`。

**第二步：启动前端交互**
直接双击或用浏览器打开 `index.html`，即可进入智能法律问答控制台。
<img width="1919" height="1015" alt="屏幕截图 2026-05-15 115212" src="https://github.com/user-attachments/assets/7ace4140-9d30-4a4e-bba1-e2d02504e274" />
<img width="1919" height="1017" alt="屏幕截图 2026-05-08 113814" src="https://github.com/user-attachments/assets/ad6a9f72-225c-4b54-864d-38133c72ff86" />

---

## 系统性能测试

项目集成了专用的压力测试模块，用于评估系统在高并发法律咨询场景下的表现。

* **运行多线程压测**（模拟10个用户同时进行并发深度咨询）：
```bash
python test.py

```


* **生成性能分析图表**：
```bash
python visual.py

```
<img width="936" height="468" alt="image" src="https://github.com/user-attachments/assets/235a1135-3f6f-43ee-9bfc-647cce350084" />



该脚本将生成直观的柱状图，对比分析单并发与多并发条件下的系统响应时延与请求成功率，为生产环境部署提供量化支撑。

---

## 法律声明与边界

本系统生成的回复均由大语言模型基于检索法条加工生成，仅供初步普法参考，不构成任何形式的正式法律意见、判决预测或代书诉状。如遇复杂司法纠纷，请务必咨询持有执业资格的专业律师。

```

```
