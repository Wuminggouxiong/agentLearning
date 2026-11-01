import time
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com",
)

def zero_shot_cot(question:str)-> str:
    #零样本思维链

    #第一步需要触发推理
    response1=client.chat.completions.create(
        model="deepseek-flash",
        messages=[
            {
                "role": "user",
                "content": f"{question}\n\n让我们一步步思考（Let's think step by step）："
            }
        ]
    )
    reasoning=response1.choices[0].message.content


    #第二步基于推理给出最终答案
    response2=client.chat.completions.create(
        model="deepseek-flash",
        messages=[
            {"role": "user", "content": f"{question}\n\n让我们一步步思考："},
            {"role": "assistant", "content": reasoning},
            {"role": "user", "content": "基于以上推理，请给出最终简洁的答案："}
        ]
    )

    return {
        "reasoning": reasoning,
        "answer": response2.choices[0].message.content
    }

result = zero_shot_cot("如果一列火车以120km/h的速度行驶，需要多少分钟才能走完180公里？")
print("推理过程：", result["reasoning"])
print("\n最终答案：", result["answer"])