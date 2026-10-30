import os
from dotenv import load_dotenv
load_dotenv()
print("读取到的APIKEY是:", os.environ.get('DEEPSEEK_API_KEY'))