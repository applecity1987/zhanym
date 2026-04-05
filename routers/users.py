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
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import SECRET_KEY

router = APIRouter(prefix="/users", tags=["users"])

GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_PASSWORD = os.getenv("GMAIL_PASSWORD")

def send_email(to_email: str, code: str):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "🌹 Zhanym — Сброс пароля"
    msg["From"] = GMAIL_USER
    msg["To"] = to_email

    html = f"""
    <html><body style="font-family:Arial,sans-serif;background:#0d0d1a;margin:0;padding:20px">
    <div style="max-width:400px;margin:0 auto;background:#16162a;border-radius:20px;padding:30px;text-align:center;border:1px solid rgba(255,77,109,.3)">
        <div style="font-size:48px;margin-bottom:16px">🌹</div>
        <h1 style="color:white;font-size:24px;margin-bottom:8px">Zhanym</h1>
        <p style="color:rgba(255,255,255,.5);margin-bottom:24px">Сброс пароля</p>
        <div style="background:rgba(255,77,109,.15);border:1px solid rgba(255,77,109,.3);border-radius:16px;padding:20px;margin-bottom:24px">
            <p style="color:rgba(255,255,255,.6);font-size:13px;margin-bottom:8px">Твой код для сброса пароля:</p>
            <div style="font-size:36px;font-weight:900;color:#ff4d6d;letter-spacing:8px">{code}</div>
        </div>
        <p style="color:rgba(255,255,255,.4);font-size:12px">Код действует 10 минут.<br>Если ты не запрашивал сброс — просто проигнорируй это письмо.</p>
    </div>
    </body></html>
    """

    msg.attach(MIMEText(html, "html"))

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(GMAIL_USER, GMAIL_PASSWORD)
        server.sendmail(GMAIL_USER, to_email, msg.as_string())

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
    gender: str = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    if name: current_user.name = name
    if age: current_user.age = age
    if city: current_user.city = city
    if bio: current_user.bio = bio
    if height: current_user.height = height
    if gender: current_user.gender = gender
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

    code = str(random.randint(100000, 999999))
    user.reset_token = code
    db.commit()

    try:
        send_email(email, code)
        return {"message": "Код отправлен на email!", "found": True}
    except Exception as e:
        return {"message": f"Ошибка отправки: {str(e)}", "found": False}

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