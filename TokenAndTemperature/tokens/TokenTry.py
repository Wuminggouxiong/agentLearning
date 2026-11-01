#Token是模型处理文本的最小单元
import tiktoken#这是OpenAI开源的分词库
import time
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com",
)

def count_tokens(text:str,model_encoding:str="cl100k_base")->int:#用deepseek相似编码替代，可能不精确
    #计算文本在指定编码方式下的token数量
    encoding=tiktoken.get_encoding(model_encoding)#根据编码名称返回一个编码器对象：获取编码器
    tokens=encoding.encode(text)#把字符串切分成token，并返回一个整数列表
    return len(tokens)

def visualize_tokens(text:str,model_encoding:str="cl100k_base"):
    #可视化token分割
    encoding=tiktoken.get_encoding(model_encoding)
    tokens=encoding.encode(text)

    print(f"文本：{text}")
    print(f"Token数量：{len(tokens)}")
    print(f"Token列表：{[encoding.decode([t]) for t in tokens]}")
    print()

# 英文分词示例
visualize_tokens("Hello, how are you today?")
# Token 列表：['Hello', ',', ' how', ' are', ' you', ' today', '?']
# Token 数量：7

# 中文分词示例（中文通常更多 Token，不同模型切词粒度差异较大）
visualize_tokens("你好，今天天气怎么样？")
# 中文每个字通常占 0.5 到 2 个 Token 不等

# 代码的 Token 计数
code = """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
"""
visualize_tokens(code)
