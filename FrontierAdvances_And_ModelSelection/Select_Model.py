def select_model(requirements: dict) -> str:
    """Agent 模型选型决策函数（2026 年 7 月 19 日版）"""

    budget = requirements.get("monthly_budget_usd", 100)
    task_type = requirements.get("task_type", "general")
    privacy = requirements.get("privacy_required", False)
    latency_ms = requirements.get("max_latency_ms", 5000)
    reasoning = requirements.get("complex_reasoning", False)
    agent_native = requirements.get("agent_native", False)

    # 决策树
    if privacy:
        if reasoning:
            return "Kimi K3 / Qwen3-235B / GLM-5.2 (自部署)"  # 开源 + 推理 + Agent
        elif latency_ms < 500:
            return "Phi-4-mini / Qwen3-4B (本地部署)"  # 端侧 SLM
        else:
            return "Qwen3-32B / Llama 5 (自部署)"  # 开源通用

    if agent_native:
        if budget > 500:
            return "Claude Opus 4.8 / GPT-5.5 / GLM-5.2"  # 顶级 Agent 体验
        else:
            return "Kimi K3 API / DeepSeek-V4.1 API / GLM-5.2 API"  # 性价比 Agent（K3 仅为 Opus 4.8 的 1/10）

    if reasoning:
        if budget > 500:
            return "Claude Opus 4.8 / GPT-5.5 / GLM-5.2"  # 顶级推理
        else:
            return "DeepSeek-V4.1 API / o4-mini"  # 性价比推理

    if budget < 50:
        return "DeepSeek-V3 API / GPT-4.1-mini"  # 极致性价比

    return "GPT-5.5 / Claude Opus 4.8 / GLM-5.2"  # 通用均衡之选
