from fastapi import WebSocket
import json


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[WebSocket, int] = {}

    async def connect(self, websocket: WebSocket, client_id: int):
        await websocket.accept()
        self.active_connections[websocket] = client_id
        await self.broadcast_user_count()

    def disconnect(self, websocket: WebSocket):
        self.active_connections.pop(websocket, None)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str, exclude: WebSocket = None):  # type: ignore
        for connection in self.active_connections:
            if connection != exclude:
                await connection.send_text(message)

    async def broadcast_user_count(self):
        count_message = json.dumps(
            {
                "type": "user_count",
                "count": len(self.active_connections),
                "dp_img": "https://fastapi.tiangolo.com/img/favicon.png",
                "user_name": "FastAPI",
            }
        )
        for connection in self.active_connections:
            await connection.send_text(count_message)


manager = ConnectionManager()
