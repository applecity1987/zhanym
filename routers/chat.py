from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from database import get_db, SessionLocal
from auth import get_current_user
import models
from datetime import datetime

router = APIRouter(prefix="/chat", tags=["chat"])

active_connections: dict = {}

@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    await websocket.accept()
    active_connections[user_id] = websocket
    db = SessionLocal()
    try:
        while True:
            data = await websocket.receive_json()
            receiver_id = data.get("receiver_id")
            message = data.get("message")

            # СОХРАНЯЕМ В БАЗУ
            msg = models.Message(
                sender_id=user_id,
                receiver_id=receiver_id,
                content=message,
                created_at=datetime.utcnow()
            )
            db.add(msg)
            db.commit()

            # ОТПРАВЛЯЕМ ПОЛУЧАТЕЛЮ
            if receiver_id in active_connections:
                await active_connections[receiver_id].send_json({
                    "sender_id": user_id,
                    "message": message,
                    "time": datetime.utcnow().isoformat()
                })
    except WebSocketDisconnect:
        if user_id in active_connections:
            del active_connections[user_id]
    finally:
        db.close()

@router.get("/history/{user_id}")
def get_history(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):

    db.query(models.Message).filter(
        models.Message.sender_id == user_id,
        models.Message.receiver_id == current_user.id,
        models.Message.is_read == False
    ).update({"is_read": True})
    db.commit()

    messages = db.query(models.Message).filter(
        ((models.Message.sender_id == current_user.id) & (models.Message.receiver_id == user_id)) |
        ((models.Message.sender_id == user_id) & (models.Message.receiver_id == current_user.id))
    ).order_by(models.Message.created_at).all()
    return messages

@router.get("/unread")
def get_unread(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    count = db.query(models.Message).filter(
        models.Message.receiver_id == current_user.id,
        models.Message.is_read == False
    ).count()
    return {"count": count}

@router.get("/unread_by_sender")
def get_unread_by_sender(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    from sqlalchemy import func
    results = db.query(
        models.Message.sender_id,
        func.count(models.Message.id).label('count')
    ).filter(
        models.Message.receiver_id == current_user.id,
        models.Message.is_read == False
    ).group_by(models.Message.sender_id).all()
    return {r.sender_id: r.count for r in results}