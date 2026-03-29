from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from database import get_db
from auth import get_current_user, hash_password
import models
import shutil
import os
import smtplib
import ssl
import secrets
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me")
def get_me(current_user: models.User = Depends(get_current_user)):
    return current_user

@router.put("/me")
def update_profile(
    name: str = None,
    age: int = None,
    city: str = None,
    bio: str = None,
    height: int = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    if name: current_user.name = name
    if age: current_user.age = age
    if city: current_user.city = city
    if bio: current_user.bio = bio
    if height: current_user.height = height
    db.commit()
    db.refresh(current_user)
    return current_user

@router.put("/me/onboarding")
def save_onboarding(
    goal: str = None,
    drink: str = None,
    smoke: str = None,
    sport: str = None,
    pet: str = None,
    communication: str = None,
    love_language: str = None,
    education: str = None,
    zodiac: str = None,
    interests: str = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    if goal: current_user.goal = goal
    if drink: current_user.drink = drink
    if smoke: current_user.smoke = smoke
    if sport: current_user.sport = sport
    if pet: current_user.pet = pet
    if communication: current_user.communication = communication
    if love_language: current_user.love_language = love_language
    if education: current_user.education = education
    if zodiac: current_user.zodiac = zodiac
    if interests: current_user.interests = interests
    db.commit()
    db.refresh(current_user)
    return {"status": "ok"}

@router.post("/me/photo")
def upload_photo(
    file: UploadFile = File(...),
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    upload_dir = "static/uploads"
    os.makedirs(upload_dir, exist_ok=True)
    filename = f"user_{current_user.id}_{file.filename}"
    filepath = f"{upload_dir}/{filename}"
    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    current_user.photo = filename
    db.commit()
    return {"photo": filename}

@router.post("/me/telegram")
def save_telegram(telegram_id: int, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    current_user.telegram_id = telegram_id
    db.commit()
    return {"message": "Telegram подключён!"}

@router.post("/forgot-password")
def forgot_password(email: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email.ilike(email)).first()
    if not user:
        return {"message": "Email не найден", "found": False}
    if not user.telegram_id:
        return {"message": "Telegram не подключён", "found": False, "no_telegram": True}

    import random
    code = str(random.randint(100000, 999999))
    user.reset_token = code
    db.commit()

    import httpx
    BOT_TOKEN = "8268233353:AAGD_d6IcNo2qOPeRViLzWJTDwkuQhWGa40"
    httpx.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        json={
            "chat_id": user.telegram_id,
            "text": f"🌹 Zhanym — Сброс пароля\\n\\nТвой код: *{code}*\\n\\nВведи его на сайте. Действует 10 минут.",
            "parse_mode": "Markdown"
        }
    )
    return {"message": "Код отправлен в Telegram!", "found": True}

@router.post("/reset-password")
def reset_password(token: str, new_password: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.reset_token == token).first()
    if not user:
        raise HTTPException(status_code=400, detail="Неверный токен")
    user.hashed_password = hash_password(new_password)
    user.reset_token = None
    db.commit()
    return {"message": "Пароль изменён!"}

@router.get("/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user

@router.post("/verify-reset-code")
def verify_reset_code(email: str, code: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email.ilike(email)).first()
    if not user or user.reset_token != code:
        raise HTTPException(status_code=400, detail="Неверный код")
    return {"message": "Код верный!"}

@router.post("/reset-password-by-code")
def reset_password_by_code(email: str, code: str, new_password: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email.ilike(email)).first()
    if not user or user.reset_token != code:
        raise HTTPException(status_code=400, detail="Неверный код")
    user.hashed_password = hash_password(new_password)
    user.reset_token = None
    db.commit()
    return {"message": "Пароль изменён!"}