from openai import OpenAI,RateLimitError,APIError,APITimeoutError
import time
import logging
import os

logger=logging.getLogger(__name__)#获取一个以当前模块名(__name__)为名称的Logger（日记记录器）对象

client = OpenAI(
    api_key=os.environ.get('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com",
)

def robust_chat(
    message:str,
    max_retries:int=3,
    retry_delay:float=1.0
)->str:
    #带重试机制的鲁棒调用
    for attempt in range(max_retries):
        try:
            response=client.chat.completions.create(
                model="deepseek-flash",
                messages=[{"role":"user","content":message}],
                timeout=30 #秒
            )
            return response.choices[0].message.content
        except RateLimitError:
            #触发速率限制，等待后重试
            wait_time=retry_delay*(2**attempt)#重试机制里常见的指数退避公式——本次重试前等待的时间 = 基础延迟 × 2 的 attempt 次方。
            logger.warning(f"触发速率限制，{wait_time}秒后重试（第{attempt+1}次")
            time.sleep(wait_time)
        except APITimeoutError:
            logger.warning(f"请求超时，重试中（第{attempt+1}次）")
        except APIError as e:
            if e.status_code>=500:#服务器错误，可以重试
                logger.error(f"API服务器错误{e.status_code}，重试中")
                time.sleep(retry_delay)
            else:
                raise RuntimeError("API调用失败") from e#重新抛出异常
    raise RuntimeError(f"API调用在{max_retries}次重试后仍然失败")

try:
    result=robust_chat("你好，今天天气怎么样？")
    print(result)
except RuntimeError as e:
    print(f"调用失败：{e}")