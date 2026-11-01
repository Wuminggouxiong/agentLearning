TEMPERATURE_GUIDE = {
    "代码生成": 0.1,          # 要求精确，低随机性
    "数据提取/JSON格式化": 0.0, # 完全确定性，防崩溃
    "问答/事实查询": 0.3,      # 稍微稳定
    "文案/摘要": 0.7,         # 平衡创意和准确
    "头脑风暴/创意": 1.0,      # 鼓励多样性
    "诗歌/创意写作": 1.2,      # 高创意
    "Agent 逻辑路由": 0.1,    # 工具调用需要极度稳定
    "对话/闲聊": 0.8,         # 自然对话
}

def get_optimal_temperature(task_type: str) -> float:
    return TEMPERATURE_GUIDE.get(task_type, 0.7)