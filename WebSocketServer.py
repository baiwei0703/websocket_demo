import asyncio
import websockets
import subprocess

async def execute_command(command):
    """执行Windows命令行命令并返回输出"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout
        else:
            return result.stderr
    except Exception as e:
        return str(e)

async def handler(websocket):
    """处理WebSocket连接"""
    async for message in websocket:
        print(f"Received command: {message}")
        output = await execute_command(message)
        await websocket.send(output)

async def start_server():
    """启动WebSocket服务器"""
    async with websockets.serve(handler, "0.0.0.0", 8765):
        print("WebSocket server started on ws://0.0.0.0:8765")
        await asyncio.Future()  # 保持服务器运行

if __name__ == "__main__":
    asyncio.run(start_server())