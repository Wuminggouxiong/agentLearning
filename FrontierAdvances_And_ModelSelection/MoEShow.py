#辅助理解混合专家架构
class MixtureOfExperts:
    """
    以 Qwen3-235B-A22B 为例：
    总参数量：235B
    每次激活：22B（仅 ~9.4%）
    效果：性能超越 DeepSeek-R1 和 OpenAI o1，推理成本仅为零头
    """
    def __init__(self,num_experts=128,active_experts=8):
        self.num_experts=num_experts#总共有这么多专家
        self.active_experts=active_experts#每个token只激活其中8个

    def forward(self,input_tokens):
        #1.Router决定激活哪些专家
        scores=self.router(input_tokens)
        top_k=scores.topk(self.active_experts)
        #2.只有被选中的专家参与计算
        #3.按权重加权求和
        return sum(expert(input_tokens)*w for expert,w in top_k)
"""
它是概念模型，真实 MoE 还有几块关键机制没体现：

Token 级路由：真实是每个 token 独立选专家，不是整段输入共用一个专家组合。

Softmax 归一化：w 通常是 top-k 分数经 softmax 后的归一化权重，保证加权和尺度稳定。

负载均衡损失（load balancing loss）：如果放任 router 自由选，它会把大部分 token 都塞给少数几个“明星专家”，导致其他专家训练不足、GPU 负载不均。所以训练时一定要加辅助损失，强迫 token 均匀分散到各专家。这是 MoE 训练最关键、也最容易翻车的地方。

容量因子（capacity factor）与 token dropping：工程实现里每个专家有固定容量上限，超出部分会被丢弃或绕行，避免某个专家被挤爆。

共享专家（shared expert）：DeepSeek-MoE 等架构会让所有 token 都过几个共享专家，再叠加路由专家，提升稳定性。

专家并行（expert parallelism）：128 个专家分布在多张 GPU 上，路由意味着跨卡通信，这是 MoE 推理/训练的主要工程难点。
"""