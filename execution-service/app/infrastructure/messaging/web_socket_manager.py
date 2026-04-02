from fastapi import WebSocket

from application.ports.socket import Socket


class WebSocketManager(Socket):

    def __init__(self):
        self.connections: dict[int, WebSocket] = {}

    async def connect(self, user_id: int, websocket: WebSocket) -> None:
        await websocket.accept()
        self.connections[user_id] = websocket

    def disconnect(self, user_id: int) -> None:
        self.connections.pop(user_id)

    async def send_json(self, user_id: int, message: dict) -> None:
        await self.connections[user_id].send_json(message)

    def get_connections(self) -> dict:
        return self.connections

websocket_manager = WebSocketManager()