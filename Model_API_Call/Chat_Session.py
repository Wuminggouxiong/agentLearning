import time
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com",
)

class ChatSession:
    #管理多轮对话历史的简单封装
    def __init__(self,system_prompt:str=None,model:str="deepseek-flash"):
        self.model=model
        self.messages=[]

        if system_prompt:
            self.messages.append({
                "role":"system",
                "content":system_prompt
            })

    def chat(self,user_message:str)->str:
        #发送消息并获取回复
        #添加用户消息
        self.messages.append({
            "role":"user",
            "content":user_message
        })
        #调用API
        response=client.chat.completions.create(
            model=self.model,
            messages=self.messages
        )
        #获取回复
        assistant_message=response.choices[0].message.content
        #保存到历史
        self.messages.append({
            "role":"assistant",
            "content":assistant_message
        })

        return assistant_message#assistant_message是最新会话，我们把它作为"assistant"添加到历史会话中

    def clear_history(self):
        #清楚历史对话，但是要保留system prompt
        system_msgs=[m for m in self.messages if m["role"]=="system"]
        self.messages=system_msgs

    def get_history(self)->list:
        #获取对话历史
        return [m for m in self.messsages if m["role"]!="system"]

# 使用示例
session = ChatSession(
    system_prompt="你是一位专业的 Python 编程导师，讲解要简洁易懂。"
)

# 多轮对话
questions = [
    "什么是装饰器？",
    "能给一个实际的使用例子吗？",
    "如何给装饰器传参数？"
]

for q in questions:
    print(f"\n用户：{q}")
    answer = session.chat(q)
    print(f"助手：{answer}")