#三个工具实现
import requests#这是Python里发生HTTP请求最常用的库

#搜索，基于duckduckgo
def search_web(query:str,num_results:int=5)->str:#依据询问，返回默认5条结果
    #调用DuckDuckGo Instant Answer API（即时答案接口） 返回文本摘要
    try:
        url="https://api.duckduckgo.com/"
        #构造URL查询参数，requests会自动将他们拼接
        params={"q":query,"format":"json","no_html":1}#把传入的query作为搜索词，要求服务器以json格式返回数据，去掉html标签
        data=requests.get(url,params=params,timeout=10).json()#向duckduckgo发送get请求，设置10秒超时，最后把json转换成字典

        results=[]
        if data.get("AbstractText"):
            results.append(f"即时答案：{data['AbstractText']}")
        for topic in data.get("RelatedTopics",[])[:num_results]:#查询并且切片，超出长度不报错
            if isinstance(topic,dict) and topic.get("Text"):
                results.append(f"{topic['Text'][:200]}")
        #str.join(iterable)是字符串方法。下面这段代码的作用是，用"\n"作分隔符，把列表里所有字符串连城一个长字符串
        return "\n".join(results) if results else f"未找到结果，建议换更具体的关键词。"
    except Exception as e:
        return f"搜索失败：{e}。请检查网络连接。"


#精确计算，用受限eval兼顾安全与功能
#eval(expression, globals, locals)把一段字符串当作Python表达式来执行
import math
def calculate(expression:str)->str:
    #用受限的eval环境执行数学表达式，避免任意代码执行
    safe_dict={
        "__builtins__":{},#关键：禁用所有内置函数
        "sqrt":math.sqrt,
        "log":math.log,
        "sin":math.sin,
        "cos":math.cos,
        "pi":math.pi,
        "e":math.e,
        "abs":abs,
        "round":round,
        #其它数学函数按需添加
    }
    try:
        result=eval(expression,safe_dict)
        return f"{expression}={result}"
    except ZeroDivisionError:
        return "计算错误：除以零"
    except Exception as e:
        return f"计算错误：{e}。请确认表达式格式正确"


#单位换算
import convertTemp
def unit_converter(value:float,from_unit:str,to_unit:str)->str:
    #支持长度、重量、温度、面积四类单位的双向换算
    conversions={
        "m":1.0,"km":1000.0,"mile":1609.344,
        "kg":1.0,"pound":0.453592,
    }
    if from_unit in ["celsius", "fahrenheit", "kelvin"]:
        # 温度需要特殊处理（非线性换算）
        return convertTemp._convert_temperature(value, from_unit, to_unit)
    if from_unit not in conversions or to_unit not in conversions:
        return f"不支持的单位：{from_unit} 或 {to_unit}"
    return f"{value} {from_unit} = {value * conversions[from_unit] / conversions[to_unit]:.6g} {to_unit}"