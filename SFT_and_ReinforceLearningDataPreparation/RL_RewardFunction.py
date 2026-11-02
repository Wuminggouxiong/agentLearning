import re
import subprocess
import tempfile
from typing import Optional

def math_reward(
        response:str,
        ground_truth:str,
        format_required:bool=True,
)->float:
    """
    数学题的规则奖励函数

    奖励组成：
    - 答案正确: +1.0
    - 答案格式正确（在 \\boxed{} 中）: +0.1
    - 有推理过程: +0.1

    总分范围: [0, 1.2]
    """
    reward=0

    #1.从\boxed{}中提取答案
    boxed_match=re.serach(r"\\boxed\{.+?)\}",response)
    if boxed_match:
        predocted=boxed_match.group(1).strip()
        reward+=0.1