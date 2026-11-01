
import time
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com",
)

def estimate_image_tokens(width:int,height:int,detail:str="auto")->int:
    #估算图像消耗的token数量
    #detail模式：
    #low：固定基础消耗，不管图像多大，通常约85token
    #high：根据图像尺寸计算，切割为多个区块，可能消耗数百到数千token
    #auto：模型自动选择

    if detail=="low":
        return 85#固定消耗

    #high detail计算规则：以512*512切割算法为例
    #限制最大边长并按比例缩放
    max_dim=max(width,height)
    if max_dim>2048:
        scale=2048/max_dim
        width=int(width*scale)
        height=int(height*scale)

    #计算需要多少个512*512块
    tiles_x=(width+511)//512#向上取整
    tiles_y=(height+511)//512
    num_tiles=tiles_x*tiles_y

    #每个块消耗特定Toke+基础Token
    total_tokens=num_tiles*170+86
    return total_tokens

#常见图像尺寸的Token消耗
print("=== 多模态图像 Token 消耗估算（high detail 模式）===")
image_sizes = [
    (256, 256,   "缩略图/图标"),
    (512, 512,   "小图"),
    (1024, 768,  "普通照片"),
    (1920, 1080, "全高清截图"),
    (4096, 2160, "4K 图像"),
]
for w, h, desc in image_sizes:
    tokens_low = estimate_image_tokens(w, h, "low")
    tokens_high = estimate_image_tokens(w, h, "high")
    print(f"  {desc} ({w}x{h})：low={tokens_low}, high={tokens_high} Token")

#遇到需要频繁处理图像的场景，现在本地代码里将图像压缩到1080p一下，或者在非OCR场景使用detail="low"