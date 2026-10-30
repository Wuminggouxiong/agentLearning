#零样本直接提问
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com",
)


def few_shot_classify(text: str) -> str:
    """少样本情感分类——通过示例引导"""

    # 精心挑选的示例（覆盖不同情况）
    examples = [
        ("这款手机拍照效果惊艳，续航也很棒！", "正面"),
        ("物流太慢了，等了两周才到，很失望。", "负面"),
        ("产品符合描述，包装完好。", "中性"),
        ("客服态度超好，问题解决得很及时，给好评！", "正面"),
        ("有点贵，但质量确实不错。", "中性"),
    ]

    # 构建 Few-shot Prompt
    few_shot_prompt = "对以下评论进行情感分类（正面/负面/中性）。\n\n"

    # 将示例传递给Prompt
    for example_text, label in examples:
        few_shot_prompt += f"评论：{example_text}\n情感：{label}\n\n"

    # 将用户的问题传递给Prompt
    few_shot_prompt += f"评论：{text}\n情感："

    response = client.chat.completions.create(
        model="deepseek-flash",
        messages=[{"role": "user", "content": few_shot_prompt}]
    )
    return response.choices[0].message.content.strip()


# Few-shot 在复杂分类任务上通常更稳定
result = few_shot_classify("简直超棒（愤怒脸）")
print(f"分类结果：{result}")

