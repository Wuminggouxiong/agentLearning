import time
import os

from TokenTry import count_tokens
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com",
)

# Token 成本计算器（价格单位：美元/百万 Token，仅供参考）
PRICE_PER_1M_TOKENS = {
    "claude-3-5-sonnet": {"input": 3.0, "output": 15.0},   # Anthropic 旗舰，逻辑最强
    "gemini-2.5-pro": {"input": 2.0, "output": 12.0},     # 超长上下文与多模态王者
    "qwen-plus": {"input": 1.2, "output": 6.0},           # 业务主力，性价比高
    "kimi-k2": {"input": 1.0, "output": 3.0},             # 适合超长文本检索提取
    "deepseek-r1": {"input": 0.55, "output": 2.19},       # 推理模型(Reasoning)性价比之王
}

def estimate_cost(
        input_text:str,
        expected_output_tokens:int,
        model:str="deepseek-r1",
)->dict:
    #估算api调用成本
    input_tokens=count_tokens(input_text)

    price=PRICE_PER_1M_TOKENS.get(model,{"input":1.0,"output":2.0})
    input_cost=(input_tokens/1_000_000)*price["input"]
    output_cost=(expected_output_tokens/1_000_000)*price["output"]

    return {
        "input_tokens": input_tokens,
        "expected_output_tokens": expected_output_tokens,
        "total_tokens": input_tokens + expected_output_tokens,
        "estimated_cost_usd": input_cost + output_cost,
        "estimated_cost_cny": (input_cost + output_cost) * 7.2  # 近似汇率
    }
# 估算成本
prompt = "请为我写一篇关于 Python 异步编程的500字文章"
cost = estimate_cost(prompt, 500, "deepseek-r1")
print(f"输入 Token：{cost['input_tokens']}")
print(f"预估总成本：¥{cost['estimated_cost_cny']:.4f}")