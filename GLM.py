from openai import OpenAI

# 智谱AI 免费配置
client = OpenAI(
    api_key="09ba18a1ad2042d0875c955a25bcbab5.8MSq01TiFZsR69MC",  # 注册后在控制台获取
    base_url="https://open.bigmodel.cn/api/paas/v4/"
)

# 法律Prompt（优化版）
system_prompt = """
你是专业法律AI咨询助手，基于中国现行法律法规作答。
约束：
1. 仅依据中国大陆现行有效法律；
2. 不预测判决、不代写诉状、不提供诉讼代理；
3. 拒绝违法/灰色/侵权咨询；
4. 回答简洁通俗、条理清晰、分点说明；
5. 结合上下文连贯回答。
"""

# 多轮上下文
messages = [{"role": "system", "content": system_prompt}]

print("===== 智谱GLM-4-Flash｜法律对话 =====")
print("输入 exit 退出\n")

while True:
    user_q = input("你：")
    if user_q.lower() == "exit":
        print("AI：对话结束")
        break
    messages.append({"role": "user", "content": user_q})
    # 调用免费模型
    response = client.chat.completions.create(
        model="GLM-4-Flash",  # 永久免费
        messages=messages,
        temperature=0.3
    )
    ai_ans = response.choices[0].message.content
    print(f"AI：{ai_ans}\n")
    messages.append({"role": "assistant", "content": ai_ans})