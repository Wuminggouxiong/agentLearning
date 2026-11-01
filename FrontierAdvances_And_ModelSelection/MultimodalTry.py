# 多模态 Agent 的典型调用方式
from openai import OpenAI
client = OpenAI()

response = client.chat.completions.create(
    model="gpt-5",  # GPT-5 原生支持多模态
    messages=[{
        "role": "user",
        "content": [
            {"type": "text", "text": "这张架构图有什么问题？请给出改进建议。"},
            {"type": "image_url", "image_url": {"url": "data:image/png;base64,..."}}
        ]
    }]
)

# GPT-5 不仅能"看懂"图片，还能生成图像、实时语音对话
