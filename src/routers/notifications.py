
from fastapi import APIRouter, WebSocket
from starlette.websockets import WebSocketDisconnect, WebSocketState

from src.utils.auth import get_current_user
from src.utils.websocket import manager

notification_router = APIRouter(prefix="/notifications", tags=["notifications"])


@notification_router.websocket("")
async def websocket_notifications(websocket: WebSocket):
    # JWT 토큰을 Sec-WebSocket-Protocol 헤더에서 가져옴
    token = websocket.headers.get("Authorization")
    user = await get_current_user(token=token.split(" ")[1])
    
    await manager.connect(user_id=user.id, ws=websocket)
    
    try:
        while websocket.client_state != WebSocketState.DISCONNECTED:
            await websocket.receive()
            
    except WebSocketDisconnect:
        await manager.disconnect(ws=websocket)
