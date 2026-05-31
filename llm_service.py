from openai import OpenAI

# 智谱GLM配置
client = OpenAI(
    api_key="198ea24aceac421fb475db66db11ed06.4YeiHHwG8BYBNEUN",
    base_url="https://open.bigmodel.cn/api/paas/v4/"
)

system_prompt = """
    你是专业法律AI咨询助手，基于中国现行法律法规作答。
    约束：
    1. 仅依据中国大陆现行有效法律；
    2. 不预测判决、不代写诉状、不提供诉讼代理；
    3. 拒绝违法/灰色/侵权咨询；
    4. 回答简洁通俗、条理清晰、分点说明；
    5. 结合上下文连贯回答。
    """

def chat_with_glm(user_question, history=None):
    try:
        messages = [{"role": "system", "content": system_prompt}]
        
        if history:
            messages.extend(history)
        
        messages.append({"role": "user", "content": user_question})

        response = client.chat.completions.create(
            model="GLM-4-Flash",
            messages=messages,
            temperature=0.3
        )

        answer = response.choices[0].message.content
        return answer

    except Exception as e:
        return f"AI出错：{str(e)}"