import websockets
import asyncio

import json

class DhcpInfo:
    def __init__(self, scope, reserved_ip, mac_address, remark, opt_type):
        self.scope = scope
        self.reserved_ip = reserved_ip
        self.mac_address = mac_address
        self.remark = remark
        self.opt_type = opt_type

    def __repr__(self):
        return f"DhcpInfo(scope={self.scope}, reserved_ip={self.reserved_ip}, mac_address={self.mac_address}, remark={self.remark}, opt_type={self.opt_type})"

    @classmethod
    def from_json(cls, json_str):
        try:
            # 将JSON字符串转为dict
            data = json.loads(json_str)
            # 使用dict的数据创建类实例
            return cls(**data)
        except TypeError:
            return None



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