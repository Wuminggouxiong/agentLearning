import time
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com",
)

def create_agent_call(
        messages: list,
        task_type: str = "general",
        **override_params
) -> dict:
    """
    Agent 调用的最佳实践封装工厂
    根据任务类型自动匹配最优的模型与参数
    """

    # 不同任务类型的动态路由预设
    task_presets = {
        "reasoning": {  # 复杂推理、逻辑 Bug 排查
            "model": "deepseek-r1",  # 使用强大的推理模型
            "temperature": 0.6,  # 推理模型自带内部探索，通常不需要过低的温度
            "max_tokens": 8000,  # 必须预留大量 Token 供其生成思考链 (CoT)
        },
        "code": {  # 纯代码编写/重构
            "model": "claude-3-5-sonnet",  # 编程天花板
            "temperature": 0.1,
            "max_tokens": 4000,
        },
        "extraction": {  # 信息提取、意图分类、JSON 生成
            "model": "kimi-k2",  # 性价比极高，处理长文本块便宜
            "temperature": 0.0,  # 杜绝任何随机性导致 JSON 解析崩溃
            "max_tokens": 500,
        },
        "creative": {  # 创意文案、脑暴
            "model": "qwen-plus",
            "temperature": 0.9,
            "max_tokens": 1000,
            "presence_penalty": 0.3,
        },
        "general": {  # 通用闲聊与常规指令
            "model": "qwen-plus",
            "temperature": 0.7,
            "max_tokens": 1500,
        }
    }

    params = task_presets.get(task_type, task_presets["general"])
    params.update(override_params)  # 允许外部业务层覆盖默认参数
    params["messages"] = messages

    response = client.chat.completions.create(**params)

    return {
        "content": response.choices[0].message.content,
        "usage": {
            "input": response.usage.prompt_tokens,
            "output": response.usage.completion_tokens,
            "total": response.usage.total_tokens
        },
        "model": response.model,
        "finish_reason": response.choices[0].finish_reason
    }


# 使用示例：要求 Agent 根据文案生成提取结论
result = create_agent_call(
    messages=[{"role": "user", "content": "从这段文字中提取用户购买意向评级..."}],
    task_type="extraction"
)
print(f"路由选用模型：{result['model']}")
print(f"Token 总消耗：{result['usage']['total']}")
