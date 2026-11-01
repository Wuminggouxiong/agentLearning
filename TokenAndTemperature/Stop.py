#自定义停止条件
import time
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com",
)

def demo_stop():
    #让模型在特定字符串处戛然而止，这招在数据提取及其省钱
    response=client.chat.completions.create(
        model="deepseek-flash",
        messages=[{"role": "user", "content": "请按格式输出：\n名称：\n价格：\n描述："}],
        stop=["描述："],#一旦生成这个词，立即强行停止API生成
    )

def extract_until_marker(text:str,stop_marker:str)->str:
    #提取直到某个标记符的内容，防止大模型后面补充寒暄废话
    response = client.chat.completions.create(
        model="kimi-k2",
        messages=[{"role": "user", "content": text}],
        stop=[stop_marker]
    )
    return response.choices[0].message.content