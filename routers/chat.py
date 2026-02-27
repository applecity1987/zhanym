from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from database import get_db
from auth import get_current_user
import models
from datetime import datetime

router = APIRouter(prefix="/chat", tags=["chat"])

# Хранение активных соединений
active_connections: dict = {}

@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    await websocket.accept()
    active_connections[user_id] = websocket
    try:
        while True:
            data = await websocket.receive_json()
            receiver_id = data.get("receiver_id")
            message = data.get("message")

            if receiver_id in active_connections:
                await active_connections[receiver_id].send_json({
                    "sender_id": user_id,
                    "message": message,
                    "time": datetime.utcnow().isoformat()
                })
    except WebSocketDisconnect:
        del active_connections[user_id]

@router.get("/history/{user_id}")
def get_history(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    messages = db.query(models.Message).filter(
        ((models.Message.sender_id == current_user.id) & (models.Message.receiver_id == user_id)) |
        ((models.Message.sender_id == user_id) & (models.Message.receiver_id == current_user.id))
    ).order_by(models.Message.created_at).all()
    return messages
