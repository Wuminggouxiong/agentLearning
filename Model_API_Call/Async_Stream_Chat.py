import asyncio
import os
from openai import AsyncOpenAI

async_client=AsyncOpenAI(
    api_key=os.environ.get('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com",
)

async def async_stream_chat(message:str)->str:
    #异步流式输出
    stream=await async_client.chat.completions.create(
        model="deepseek-flash",
        messages=[{"role":"user","content":message}],
        stream=True
    )

    full_response=""
    async for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            content=chunk.choices[0].delta.content
            print(content,end="",flush=True)
            full_response+=content

    return full_response

asyncio.run(async_stream_chat("解释一下什么是异步编程"))