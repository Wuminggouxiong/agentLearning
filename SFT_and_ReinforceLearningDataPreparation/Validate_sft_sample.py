#典型的SFT样本结构大概是这样的
'''
{
  "conversations": [
    {"role": "system", "content": "..."},
    {"role": "user", "content": "..."},
    {"role": "assistant", "content": "<think>...</think><tool_call>...</tool_call>"}
  ]
}
'''

import re
import json
from collections import Counter

def validate_sft_sample(sample:dict)->dict:
    #对单条SFT样本进行多维度质量检测
    issues=[]
    conversations=sample.get("conversations",[])

    #1.基础结构检查
    #检查第一句必是system，且至少有一条assistant回答
    roles=[msg["role"] for msg in conversations]
    if not roles or roles[0]!="system":
        issues.append("缺少system消息")
    if "assistant" not in roles:
        issues.append("缺少assistant回答")

    #2.格式一致性检查（Agent场景）
    #只检查assistant消息内容，因为这类标签通常只出现在模型输出里
    for msg in conversations:
        if msg["role"]=="assistant":
            content=msg["content"]

            #检查think标签配对
            think_opens=len(re.findall(r"<think>",content))
            think_closes=len(re.findall(r"</think>",content))#统计标签出现的次数
            if think_closes!=think_opens:
                issues.append(f"think 标签不配对：{think_opens} 开 vs {think_closes} 闭")

            # 检查 tool_call 标签配对
            tc_opens = len(re.findall(r"<tool_call>", content))
            tc_closes = len(re.findall(r"</tool_call>", content))
            if tc_opens != tc_closes:
                issues.append(f"tool_call 标签不配对: {tc_opens} 开 vs {tc_closes} 闭")

            #检查工具调用格式
            tool_calls=re.findall(
                r"<tool_call>\n(.+?)\n</tool_call>",content,re.DOTALL
            )
            for tc in tool_calls:
                #验证是否为合法的函数调用格式
                if not re.match(r"\w+\(.*\)",tc.strip()):
                    issues.append(f"工具调用格式异常：{tc[:50]}")#只截取前50字符用作报错展示

    #3.长度合理性检查
    total_tokens=sum(len(msg["content"]) for msg in conversations)
    if total_tokens<50:
        issues.append("样本过短，可能缺乏信息量")
    if total_tokens>20000:
        issues.append("样本过长，可能包含冗余内容")

    #4.回答非空检查
    assistant_msgs=[m for m in conversations if m["role"]=="assistant"]
    for i,msg in enumerate(assistant_msgs):
        if len(msg["content"].strip())<10:
            issues.append(f"第{i+1}个assistant回答过短")


    return {
        "valid": len(issues) == 0,
        "issues": issues,
        "num_turns": len(assistant_msgs),
        "total_chars": total_tokens
    }
'''
SFT数据内部的标签是干嘛的：
这类SFT数据通常是给Agent模型或者推理模型训练用，
<think>/</think>是思维链标记，内部是思考过程
<tool_call>/</tool_call>是工具调用标记，有两种格式约定，一是类似函数调用，二是JSON，我们的代码就是函数调用的格式

补充一下正则表达式的基础
<think> 普通字符，照原样匹配
\w      一个“单词字符”：字母、数字、下划线
\w+     一个或多个单词字符，例如get_weather
\(和\)  都是真正的左右括号，只有括号有特殊含义
.       任意一个字符，默认不包括换行
.*      任意个字符，贪婪，尽量多匹配
.+?     至少一个字符，非贪婪，尽量少匹配
re.DOTALL 让.也能匹配换行符

出现的函数/方法：
1. re.findall(pattern, string, flags)：
    在 string 中找出所有匹配 pattern 的内容，返回一个列表（没匹配到就是空列表）。
2. re.match(pattern, string)：
    从字符串开头尝试匹配，匹配到返回 Match 对象（真值），否则返回 None（假值）。
3.enumerate(list)：遍历时同时拿到“下标”和“元素”。
'''

def analyze_dataset_distribution(samples:list[dict])->dict:
    #分析数据集的整体分布特征
    turn_counts=[
        len([m for m in s["conversations"] if m["role"=="assistant"]]) for s in samples
    ]

    #统计工具调用覆盖率
    tool_usage=Counter()
    for s in samples:
        for msg in s["conversations"]:
            if msg["role"]=="assistant":
                tools=re.findall(r"(\w+)\(",msg["content"])
                tool_usage.update(tools)
    #统计长度分布
    lengths=[
        sum(len(m["content"])for m in s["conversations"])for s in samples
    ]
    return {
        "total_samples": len(samples),
        "avg_turns": sum(turn_counts) / len(turn_counts),
        "max_turns": max(turn_counts),
        "tool_coverage": dict(tool_usage.most_common(20)),
        "avg_length": sum(lengths) / len(lengths),
        "length_p90": sorted(lengths)[int(len(lengths) * 0.9)],
    }
