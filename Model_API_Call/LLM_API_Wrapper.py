#封装统一的LLM客户端
from enum import Enum
from dataclasses import dataclass
from typing import Optional,Generator
import os

from openai import OpenAI

#把提供商这个固定选项集合起来，避免到处写裸字符串
class ModelProvider(Enum):
    #用来定义枚举类型，也就是一组有名字的常量
    #好处是：比直接写字符串更安全、可读性更好、IDE 能补全，也不容易拼错。在 LLM 封装里常用来表示角色、消息类型、模型提供商等固定选项。
    OPENAI="openai"
    OLLAMA="ollama"
    QWEN="qwen"
    DEEPSEEK="deepseek"
    ZHIPU="zhipu"

#一个装饰类，用来快速定义数据类，我们只写字段，它自动生成__init__ __repr__ __eq__等方法
@dataclass
#配置数据类
class LLMConfig:
    provider:ModelProvider
    model:str
    temperature:float=0.7
    max_tokens:int=2000
    timeout:int=30

class UnifiedLLMClient:
    # 统一的LLM调用客户端，支持多个提供商
    def __init__(self,config:LLMConfig):
        self.config=config#保存配置
        self.client=self._create_client()#调用我们写的核心分发逻辑

    #用字典把每个提供商的api_key和base_url映射好
    #根据config.provider取出对应配置
    #再用OpenAI创建客户端
    def _create_client(self)->OpenAI:
        configs={
            ModelProvider.OPENAI: {
                "api_key": os.getenv("OPENAI_API_KEY"),
                "base_url": None
            },
            ModelProvider.OLLAMA: {
                "api_key": "ollama",
                "base_url": "http://localhost:11434/v1"
            },
            ModelProvider.QWEN: {
                "api_key": os.getenv("DASHSCOPE_API_KEY"),
                "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1"
            },
            ModelProvider.DEEPSEEK: {
                "api_key": os.getenv("DEEPSEEK_API_KEY"),
                "base_url": "https://api.deepseek.com"
            },
            ModelProvider.ZHIPU: {
                "api_key": os.getenv("ZHIPU_API_KEY"),
                "base_url": "https://open.bigmodel.cn/api/paas/v4/"
            }
        }

        provider_config=configs[self.config.provider]
        #过滤掉值为None的项
        #*把列表/原组拆成位置参数 **把字典拆成关键词参数
        # def g(x, y):
        #     print(x, y)
        #
        # g(*[1, 2])  # 等价于 g(1, 2)
        # g(**{"x": 1, "y": 2})  # 等价于 g(x=1, y=2)
        return OpenAI(**{k:v for k,v in provider_config.items() if v is not None})

    def chat(self, messages: list, stream: bool = False):
        """统一的对话接口"""
        kwargs = {
            "model": self.config.model,
            "messages": messages,
            "temperature": self.config.temperature,
            "max_tokens": self.config.max_tokens,
            "stream": stream
        }

        return self.client.chat.completions.create(**kwargs)

    def simple_chat(self, message: str, system: str = None) -> str:
        """简单的单轮对话"""
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": message})

        response = self.chat(messages)
        return response.choices[0].message.content

deepseek_llm = UnifiedLLMClient(LLMConfig(
    provider=ModelProvider.DEEPSEEK,
    model="deepseek-flash",
    temperature=0.7
))
# 无论哪个提供商，接口完全一致
result = deepseek_llm.simple_chat("Python 和 JavaScript 的主要区别是什么？")
print(result)