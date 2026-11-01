import time
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com",
)

def generate_multiple_options(prompt:str,n:int=3)->list:
    results=[]
    for _ in range(n):
        response = client.chat.completions.create(
            model="deepseek-flash",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.9,
            # n 不传，默认就是 1
        )
        results.append(response.choices[0].message.content)
    return results

#deepseek的ChatCompletions接口只支持n=1，不支持一次返回多个候选
"""
def generate_multiple_options(prompt:str,n:int=3)->list:
    #一次API调用生成多个平行候选结果，供业务下游做选择或打分
    response=client.chat.completions.create(
        model="deepseek-flash",
        messages=[{"role":"user","content":prompt}],
        n=n,#生成n个不同分支的回复
        temperature=0.9#必须调高temperature确保不同分支的多样性
    )
    return [choice.message.content for choice in response.choices]
"""
# 适合：广告文案标题生成、A/B测试方案、多 Agent 辩论初稿
titles = generate_multiple_options(
    "为一篇关于 Agent 多智能体协同的技术博客生成3个吸引人的标题",
    n=3
)
for i, title in enumerate(titles, 1):
    print(f"候选 {i}：{title}")