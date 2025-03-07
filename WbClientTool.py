import websockets
import asyncio


class WebSocketClient:
    def __init__(self, url):
        self.url = url

    async def send_command(self, command):
        try:
            async with websockets.connect(self.url) as websocket:
                await websocket.send(command)
                response = await websocket.recv()
            return response
        except websockets.exceptions.ConnectionClosedError as e:
            print(f"Connection closed unexpectedly: {e}. Reconnecting...")
            await asyncio.sleep(1)  # 等待1秒后重试
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return


if __name__ == '__main__':
    client = WebSocketClient("ws://192.168.9.230:8765")
    result = asyncio.run(client.send_command("ipconfig"))
    print(result)