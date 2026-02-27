from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from database import get_db
from auth import get_current_user, hash_password
import models
import shutil
import os

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
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    if name: current_user.name = name
    if age: current_user.age = age
    if city: current_user.city = city
    if bio: current_user.bio = bio
    db.commit()
    db.refresh(current_user)
    return current_user

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

@router.get("/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user
