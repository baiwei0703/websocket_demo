import asyncio
import websockets
import subprocess
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