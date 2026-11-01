import time
import os
from openai import OpenAI
from pyexpat.errors import messages

client = OpenAI(
    api_key=os.environ.get('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com",
)

def stream_chat(message:str,system:str=None)->str:
    # 流式输出实时打印生成内容
    messages=[]
    if system:
        messages.append({"role":"system","content":system})
    messages.append({"role":"user","content":message})

    stream=client.chat.completions.create(
        model="deepseek-flash",
        messages=messages,
        stream=True#stream=True开启流式模式
    )

    full_response=""
    print("助手：",end="",flush=True)#结尾没有换行，需要flush把缓冲区的内容压出去

    for chunk in stream:
        #每个chunk包含一小段文本
        if chunk.choices[0].delta.content is not None:
            content=chunk.choices[0].delta.content
            print(content,end="",flush=True)
            full_response+=content

    print()#换行
    return full_response

# 测试流式输出
result = stream_chat("写一篇4000字左右的科幻小说，有深度有内涵")
print(f"\n完整内容（{len(result)} 字）")
