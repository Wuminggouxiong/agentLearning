#temperature控制输出的随机性，是最重要的参数之一


import time
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com",
)

def test_temperature(prompt:str,temperatures:list,runs:int=3):
    #对比不同temperature输出效果

    for temp in temperatures:
        print(f"\n{'='*50}")
        print(f"Temperature = {temp}")
        print('='*50)

        for i in range(runs):
            response=client.chat.completions.create(
                model="deepseek-flash",
                messages=[{"role":"user","content":prompt}],
                temperature=temp,
                max_tokens=1024#对deepseek这类思考模型，调大maxtoken，留出思考空间
            )

            print(f"运行{i+1}:{response.choices[0].message.content}")

# 测试创意写作（高 Temperature 更好）
test_temperature(
    "用一句话描述春天",
    temperatures=[0.0, 0.7, 1.5],#t=0不保证完全稳定输出，但语义层面能保证基本收敛
    runs=3
)