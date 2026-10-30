from Prompt.ToTOriginal import Tree_of_Thought
from Prompt.ToTOriginal.Tree_of_Thought import tree_of_thought


def autoTry(problem:str)->int:
    GeneratePaths=f"""
        问题：{problem}
        请根据问题提供最适合的几条思维路径的条数
    """
    pathsNumber= Tree_of_Thought.client.chat.completions.create(
        model="deepseek-flash",
        messages=[{"role":"user","content":GeneratePaths}]
    )
    return pathsNumber.choices[0].message.content

problem = """
我需要在3个月内学习 Python，用于数据分析工作。
我每天只有2小时学习时间，有一定的编程基础（学过简单的 HTML/CSS）。
应该如何规划学习路径？
"""

result=tree_of_thought(problem,autoTry(problem));
print("多路径探索：\n", result["paths"])
print("\n评估与推荐：\n", result["evaluation"])