import time
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com",
)

def benchmark_strategies(question: str) -> dict:
    """对比不同策略在同一问题上的效果"""

    strategies = {
        "zero_shot": {
            "messages": [{"role": "user", "content": question}]
        },
        "cot": {
            "messages": [{"role": "user", "content": f"{question}\n\n让我们一步步思考："}]
        },
        "few_shot_cot": {
            "messages": [
                {
                    "role": "system",
                    "content": "你是一个逻辑推理专家，解题时先分析条件，再逐步推导。"
                },
                {
                    "role": "user",
                    "content": """示例：
                        问题：5个人分12个苹果，平均每人得几个？
                        分析：总量12，人数5，做除法
                        计算：12 ÷ 5 = 2.4
                        答案：平均每人得 2.4 个苹果

                        现在解答：""" + question
                }
            ]
        }
    }

    results = {}
    for name, config in strategies.items():
        start = time.time()
        response = client.chat.completions.create(
            model="deepseek-flash",
            **config
        )
        elapsed = time.time() - start

        results[name] = {
            "answer": response.choices[0].message.content,
            "tokens": response.usage.total_tokens,
            "time": f"{elapsed:.2f}s"
        }

    return results


# 测试复杂推理问题
question = "一个班级有40名学生，其中60%喜欢数学，75%喜欢语文。至少有多少名学生同时喜欢数学和语文？"
results = benchmark_strategies(question)

for strategy, data in results.items():
    print(f"\n策略：{strategy}")
    print(f"Token 消耗：{data['tokens']}")
    print(f"耗时：{data['time']}")
    print(f"回答：{data['answer'][:200]}...")
