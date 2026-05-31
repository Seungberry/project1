from openai import OpenAI

# 通义千问KEY
API_KEY = "sk-be42b2c30a0d4892a5c34a4b05754b4e"

client = OpenAI(
    api_key=API_KEY,
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

# 系统提示词
system_prompt = """
你是专业法律咨询助手，遵守规则：
1. 依据中国现行法律回答
2. 不提供具体司法判决、不代书诉讼
3. 不提供违法建议
4. 回答简洁、准确、通俗
"""

# 多轮对话上下文（核心）
messages = [{"role": "system", "content": system_prompt}]

print("===== 法律AI聊天机器人（输入 exit 退出）=====\n")

while True:
    # 用户输入
    user_input = input("你：")

    # 退出
    if user_input.lower() == "exit":
        print("AI：再见！")
        break

    # 把用户问题加入上下文
    messages.append({"role": "user", "content": user_input})

    # 请求模型
    response = client.chat.completions.create(
        model="qwen-turbo",
        messages=messages,
        temperature=0.3,
        max_tokens=1024
    )

    # 获取回答
    answer = response.choices[0].message.content

    # 输出AI回答（干净聊天格式）
    print("AI：", answer, "\n")

    # 把AI回答也加入上下文
    messages.append({"role": "assistant", "content": answer})