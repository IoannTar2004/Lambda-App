from fastapi import APIRouter
from starlette.websockets import WebSocket, WebSocketDisconnect

from infrastructure.messaging.web_socket_manager import websocket_manager

log_router = APIRouter(prefix="/api/log", tags=["Logging with WebSocket"])

@log_router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    user_id = 300904
    await websocket_manager.connect(user_id, websocket)
    try:
        print("WebSocket connected")
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        await websocket_manager.disconnect(user_id, websocket)
        print("WebSocket disconnected")

# @log_router.get("/run_logs")
# async def run_logs(websocket: WebSocket):