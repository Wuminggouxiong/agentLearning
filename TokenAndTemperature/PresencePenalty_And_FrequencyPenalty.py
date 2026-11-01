#persence penalty的核心机制是，只要一个词露过面，再次使用它的概率都会被施加一个固定的惩罚
#frequency的惩罚是定量的，只关心一个词出现了多少次，重复越多，惩罚越重

import time
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com",
)

def demo_penalties():
    response=client.chat.completions.create(
        model="deepseek-flash",
        messages=[{"role":"user","content":"列举10种不同的创业方向"}],

        presence_penalty=0.5,
        frequency_penalty=0.3
    )