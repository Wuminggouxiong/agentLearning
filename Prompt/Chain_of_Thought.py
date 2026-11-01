#通过让模型展示推理过程，显著提升其在复杂问题上的准确率
import time
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com",
)

def solve_with_cot(problem:str)->str:
    #使用思维连解决复杂问题
    response=client.chat.completions.create(
        model="deepseek-flash",
        messages=[
            {
                "role": "system",
                "content": """解题时，请严格按照以下步骤：
                    1. 理解问题（用1-2句话复述问题）
                    2. 分析已知条件
                    3. 制定解题思路
                    4. 逐步推导
                    5. 得出结论并验证

                    每一步都要明确标注。"""
            },
            {
                "role": "user",
                "content": problem
            }
        ]
    )
    return response.choices[0].message.content

# 数学推理问题
problem = """
小明有若干个苹果。他先给了小红苹果总数的一半多1个，又给了小李苹果总数的四分之一，
此时小明还剩9个苹果。请问小明最初有多少个苹果？
"""

result=solve_with_cot(problem)
print(result)