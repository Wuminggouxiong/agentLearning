#Top-p也叫Nucleus Sampling，从概率最高的词集合中动态截取并采样，集合大小由p决定

import time
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com",
)

#Top-p于Temperature的配合使用
response=client.chat.completions.create(
    model="deepseek-flash",
    messages=[{"role": "user", "content": "写一个关于 AI 觉醒的短故事开头"}],
    temperature=0.8,
    top_p=0.9,#只从概率总和前90%的核心词汇中选择
    max_tokens=1024
)