
from fastapi import WebSocket


class WebSocketConnectionManager:
    def __init__(self) -> None:
        self.active_connections: dict[int, WebSocket] = {}
    
    async def connect(self, user_id: int, ws: WebSocket) -> None:
        await ws.accept()
        self.active_connections[user_id] = ws
    
    async def close(self, ws: WebSocket, code: int = 1000, reason: str | None = None) -> None:
        await ws.send({"type": "websocket.close", "code": code, "reason": reason or ""})
        await self.disconnect(ws=ws)

    async def disconnect(self, ws: WebSocket) -> None:
        for user_id, conn in list(self.active_connections.items()):
            if conn == ws:
                del self.active_connections[user_id]
                break
        
    def get_user_connection(self, user_id: int) -> WebSocket | None:
        if user_id not in self.active_connections:
            return None
        return self.active_connections[user_id]

    async def send_notification(self, user_id: int, message: str) -> None:
        ws = self.get_user_connection(user_id=user_id)
        if ws:
            await ws.send_json(data={"message": message})


manager = WebSocketConnectionManager()
