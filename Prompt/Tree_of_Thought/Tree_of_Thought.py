import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com",
)


def tree_of_thought(problem: str, num_paths: int = 3) -> str:
    """
    思维树：生成多条推理路径，评估并选择最优解
    适用于复杂决策问题
    """

    # 步骤1：生成多条推理路径
    paths_prompt = f"""
        问题：{problem}

        请提供 {num_paths} 种不同的解决思路（每种思路用简短的标题开头，然后描述核心方法）：
        """

    paths_response = client.chat.completions.create(
        model="deepseek-flash",
        messages=[{"role": "user", "content": paths_prompt}]
    )

    paths = paths_response.choices[0].message.content

    # 步骤2：评估各路径
    eval_prompt = f"""
        问题：{problem}

        以下是几种解决思路：
        {paths}

        请评估每种思路的：
        1. 可行性（1-10分）
        2. 时间成本
        3. 潜在风险

        最终推荐哪种方案并说明原因。
        """

    eval_response = client.chat.completions.create(
        model="deepseek-flash",
        messages=[{"role": "user", "content": eval_prompt}]
    )

    return {
        "paths": paths,
        "evaluation": eval_response.choices[0].message.content
    }


# 示例：复杂决策问题
problem = """
我需要在3个月内学习 Python，用于数据分析工作。
我每天只有2小时学习时间，有一定的编程基础（学过简单的 HTML/CSS）。
应该如何规划学习路径？
"""

result = tree_of_thought(problem)
print("多路径探索：\n", result["paths"])
print("\n评估与推荐：\n", result["evaluation"])
