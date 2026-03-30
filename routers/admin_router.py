from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from sqlalchemy import func, text
from database import get_db
import models

router = APIRouter(prefix="/admin", tags=["admin"])

ADMIN_PASSWORD = "zhanym_admin_2024"  # Смени на свой пароль!

def check_admin(request: Request):
    token = request.cookies.get("admin_token")
    if token != ADMIN_PASSWORD:
        raise HTTPException(status_code=401, detail="Unauthorized")

# ===== СТАТИСТИКА =====
@router.get("/api/stats")
def get_stats(request: Request, db: Session = Depends(get_db)):
    check_admin(request)
    total = db.query(models.User).count()
    males = db.query(models.User).filter(models.User.gender == "male").count()
    females = db.query(models.User).filter(models.User.gender == "female").count()
    blocked = db.query(models.User).filter(models.User.is_blocked == True).count()

    # Подписки
    silver_m = db.query(models.User).filter(models.User.gender=="male", models.User.subscription=="silver").count()
    silver_f = db.query(models.User).filter(models.User.gender=="female", models.User.subscription=="silver").count()
    gold_m = db.query(models.User).filter(models.User.gender=="male", models.User.subscription=="gold").count()
    gold_f = db.query(models.User).filter(models.User.gender=="female", models.User.subscription=="gold").count()
    almaz_m = db.query(models.User).filter(models.User.gender=="male", models.User.subscription=="almaz").count()
    almaz_f = db.query(models.User).filter(models.User.gender=="female", models.User.subscription=="almaz").count()

    # Лайки
    total_likes = db.query(models.Like).count() if hasattr(models, 'Like') else 0

    return {
        "total": total,
        "males": males,
        "females": females,
        "blocked": blocked,
        "total_likes": total_likes,
        "subscriptions": {
            "silver": {"male": silver_m, "female": silver_f},
            "gold": {"male": gold_m, "female": gold_f},
            "almaz": {"male": almaz_m, "female": almaz_f},
        }
    }

# ===== СПИСОК ПОЛЬЗОВАТЕЛЕЙ =====
@router.get("/api/users")
def get_users(request: Request, db: Session = Depends(get_db), search: str = "", gender: str = ""):
    check_admin(request)
    q = db.query(models.User)
    if search:
        q = q.filter(
            (models.User.name.ilike(f"%{search}%")) |
            (models.User.username.ilike(f"%{search}%")) |
            (models.User.email.ilike(f"%{search}%"))
        )
    if gender:
        q = q.filter(models.User.gender == gender)
    users = q.order_by(models.User.id.desc()).all()
    return [
        {
            "id": u.id,
            "name": u.name,
            "username": u.username,
            "email": u.email,
            "age": u.age,
            "gender": u.gender,
            "city": u.city,
            "photo": u.photo,
            "bio": getattr(u, 'bio', ''),
            "goal": getattr(u, 'goal', ''),
            "subscription": getattr(u, 'subscription', None),
            "is_blocked": getattr(u, 'is_blocked', False),
            "telegram_id": getattr(u, 'telegram_id', None),
        }
        for u in users
    ]

# ===== ДЕТАЛИ ПОЛЬЗОВАТЕЛЯ =====
@router.get("/api/user/{user_id}")
def get_user_detail(user_id: int, request: Request, db: Session = Depends(get_db)):
    check_admin(request)
    u = db.query(models.User).filter(models.User.id == user_id).first()
    if not u:
        raise HTTPException(status_code=404, detail="Not found")

    # Лайки которые он поставил
    likes_given = []
    if hasattr(models, 'Like'):
        given = db.query(models.Like).filter(models.Like.liker_id == user_id).all()
        for l in given:
            target = db.query(models.User).filter(models.User.id == l.liked_id).first()
            if target:
                likes_given.append({"id": target.id, "name": target.name, "username": target.username})

    # Лайки которые он получил
    likes_received = []
    if hasattr(models, 'Like'):
        received = db.query(models.Like).filter(models.Like.liked_id == user_id).all()
        for l in received:
            liker = db.query(models.User).filter(models.User.id == l.liker_id).first()
            if liker:
                likes_received.append({"id": liker.id, "name": liker.name, "username": liker.username})

    # Переписка
    messages = []
    if hasattr(models, 'Message'):
        msgs = db.query(models.Message).filter(
            (models.Message.sender_id == user_id) | (models.Message.receiver_id == user_id)
        ).order_by(models.Message.id.desc()).limit(50).all()
        for m in msgs:
            sender = db.query(models.User).filter(models.User.id == m.sender_id).first()
            receiver = db.query(models.User).filter(models.User.id == m.receiver_id).first()
            messages.append({
                "id": m.id,
                "sender": sender.name if sender else "?",
                "receiver": receiver.name if receiver else "?",
                "content": m.content,
                "is_me": m.sender_id == user_id,
            })

    return {
        "id": u.id, "name": u.name, "username": u.username,
        "email": u.email, "age": u.age, "gender": u.gender,
        "city": u.city, "photo": u.photo,
        "bio": getattr(u, 'bio', ''),
        "goal": getattr(u, 'goal', ''),
        "zodiac": getattr(u, 'zodiac', ''),
        "sport": getattr(u, 'sport', ''),
        "subscription": getattr(u, 'subscription', None),
        "is_blocked": getattr(u, 'is_blocked', False),
        "telegram_id": getattr(u, 'telegram_id', None),
        "phone": getattr(u, 'phone', None),
        "likes_given": likes_given,
        "likes_received": likes_received,
        "messages": messages,
        "password_hash": u.hashed_password,
    }

# ===== БЛОКИРОВКА =====
@router.post("/api/user/{user_id}/block")
def block_user(user_id: int, request: Request, db: Session = Depends(get_db)):
    check_admin(request)
    u = db.query(models.User).filter(models.User.id == user_id).first()
    if not u:
        raise HTTPException(status_code=404, detail="Not found")
    if not hasattr(u, 'is_blocked'):
        raise HTTPException(status_code=400, detail="is_blocked field not in model")
    u.is_blocked = not u.is_blocked
    db.commit()
    return {"blocked": u.is_blocked}

# ===== ЛОГИН =====
@router.post("/api/login")
async def admin_login(request: Request):
    from fastapi.responses import JSONResponse
    data = await request.json()
    if data.get("password") == ADMIN_PASSWORD:
        response = JSONResponse({"ok": True})
        response.set_cookie("admin_token", ADMIN_PASSWORD, httponly=True, max_age=86400*7)
        return response
    raise HTTPException(status_code=401, detail="Неверный пароль")

@router.get("/api/logout")
def admin_logout():
    from fastapi.responses import JSONResponse
    response = JSONResponse({"ok": True})
    response.delete_cookie("admin_token")
    return response


# ===== ВСЕ СООБЩЕНИЯ =====
@router.get("/api/messages")
def get_all_messages(request: Request, db: Session = Depends(get_db)):
    check_admin(request)
    msgs = db.query(models.Message).order_by(models.Message.id.desc()).limit(500).all()
    return [{"id":m.id,"sender_id":m.sender_id,"receiver_id":m.receiver_id,"content":m.content} for m in msgs]

# ===== ВСЕ ЛАЙКИ =====
@router.get("/api/likes")
def get_all_likes(request: Request, db: Session = Depends(get_db)):
    check_admin(request)
    likes = db.query(models.Like).order_by(models.Like.id.desc()).all()
    result = []
    for l in likes:
        reverse = db.query(models.Like).filter(models.Like.liker_id==l.liked_id, models.Like.liked_id==l.liker_id).first()
        result.append({"id":l.id,"liker_id":l.liker_id,"liked_id":l.liked_id,"is_match":bool(reverse)})
    return result