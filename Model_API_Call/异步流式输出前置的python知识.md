async def就是定义一个异步函数（协程函数），声明这个函数是异步的，里面可以用await让出控制权，但调用它不会立刻执行
函数体里的写法也随之升级：

普通函数	异步函数
def	async def
x = f()	x = await f()（调用别的异步函数要 await）
for x in it:	async for x in it:（遍历异步迭代器）
with ...:	async with ...:（异步上下文管理器）