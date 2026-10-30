#零样本直接提问
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com",
)

def zero_shot_classify(text:str)->str:
    response=client.chat.completions.create(
        model="deepseek-flash",
        messages=[
            {
                "role": "system",
                "content": "你是一个文本分类专家。"
            },
            {
                "role": "user",
                "content": f"""
                            对以下评论进行情感分类，只返回：正面、负面、中性 之一。
                            评论：{text}
                            分类结果："""
            }
        ]
    )
    return response.choices[0].message.content.strip()

texts = [
    "这个产品太棒了，完全超出了我的预期！",
    "还可以吧，没什么特别的。",
    "质量很差，完全浪费钱，不推荐。"
]

for text in texts:
    result = zero_shot_classify(text)
    print(f"文本: {text[:20]}... → {result}")