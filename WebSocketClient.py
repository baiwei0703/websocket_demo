import asyncio
import websockets
from WbClientTool import WebSocketClient

async def send_command():
    """连接到WebSocket服务器并发送命令"""
    uri = "ws://192.168.9.230:8765"
    while True:
        try:
            async with websockets.connect(uri) as websocket:
                while True:
                    command = input("Enter command to execute (or 'exit' to quit): ")
                    if command.lower() == 'exit':
                        return
                    await websocket.send(command)
                    print(f"Sent command: {command}")
                    response = await websocket.recv()
                    print(f"Received response: {response}")
        except websockets.exceptions.ConnectionClosedError as e:
            print(f"Connection closed unexpectedly: {e}. Reconnecting...")
            await asyncio.sleep(1)  # 等待1秒后重试
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return

if __name__ == "__main__":
    asyncio.run(send_command())
