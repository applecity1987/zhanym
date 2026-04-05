from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from database import get_db
from auth import get_current_user
import models
import os
import httpx

router = APIRouter(prefix="/subscriptions", tags=["subscriptions"])

PADDLE_API_KEY = os.getenv("PADDLE_API_KEY")

# Price ID → план
PRICE_TO_PLAN = {
    "pri_01knfcwtsjdv5drrqpsrafp9kt": "silver",
    "pri_01knfd22htctsgbq5ejseejakf": "gold",
    "pri_01knfd4kjx32ty6nnmgwh8zcc7": "almaz",
}

@router.post("/activate")
async def activate_subscription(
    request: Request,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    body = await request.json()
    transaction_id = body.get("transaction_id")
    if not transaction_id:
        raise HTTPException(status_code=400, detail="transaction_id required")

    # Проверяем транзакцию через Paddle API
    async with httpx.AsyncClient() as client:
        res = await client.get(
            f"https://api.paddle.com/transactions/{transaction_id}",
            headers={"Authorization": f"Bearer {PADDLE_API_KEY}"}
        )

    if res.status_code != 200:
        raise HTTPException(status_code=400, detail="Неверная транзакция")

    data = res.json()
    status = data.get("data", {}).get("status")
    if status != "completed":
        raise HTTPException(status_code=400, detail="Транзакция не завершена")

    # Определяем план
    items = data.get("data", {}).get("items", [])
    plan = "silver"
    for item in items:
        price_id = item.get("price", {}).get("id")
        if price_id in PRICE_TO_PLAN:
            plan = PRICE_TO_PLAN[price_id]
            break

    # Активируем подписку пользователю
    current_user.subscription = plan
    current_user.subscription_active = True
    db.commit()

    return {"status": "ok", "plan": plan}


@router.post("/webhook")
async def paddle_webhook(request: Request, db: Session = Depends(get_db)):
    """Webhook от Paddle — автоматическое управление подпиской"""
    body = await request.json()
    event_type = body.get("event_type")
    data = body.get("data", {})

    if event_type == "subscription.activated":
        # Найти пользователя по email
        customer_email = data.get("customer", {}).get("email")
        user = db.query(models.User).filter(models.User.email == customer_email).first()
        if user:
            items = data.get("items", [])
            for item in items:
                price_id = item.get("price", {}).get("id")
                if price_id in PRICE_TO_PLAN:
                    user.subscription = PRICE_TO_PLAN[price_id]
                    user.subscription_active = True
                    break
            db.commit()

    elif event_type in ("subscription.canceled", "subscription.paused"):
        customer_email = data.get("customer", {}).get("email")
        user = db.query(models.User).filter(models.User.email == customer_email).first()
        if user:
            user.subscription_active = False
            db.commit()

    return {"status": "ok"}