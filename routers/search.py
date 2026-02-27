from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from database import get_db
from auth import get_current_user
import models

router = APIRouter(prefix="/search", tags=["search"])

@router.get("/")
def search_users(
    gender: str = None,
    min_age: int = None,
    max_age: int = None,
    city: str = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    query = db.query(models.User).filter(models.User.id != current_user.id)

    if gender:
        query = query.filter(models.User.gender == gender)
    if min_age:
        query = query.filter(models.User.age >= min_age)
    if max_age:
        query = query.filter(models.User.age <= max_age)
    if city:
        query = query.filter(models.User.city.ilike(f"%{city}%"))

    users = query.limit(20).all()
    return users

@router.get("/matches")
def get_matches(current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    i_liked = [r[0] for r in db.query(models.Like.liked_id).filter(models.Like.liker_id == current_user.id).all()]
    liked_me = [r[0] for r in db.query(models.Like.liker_id).filter(models.Like.liked_id == current_user.id).all()]
    match_ids = list(set(i_liked) & set(liked_me))
    matches = db.query(models.User).filter(models.User.id.in_(match_ids)).all()
    return [{"id": u.id, "name": u.name, "age": u.age, "gender": u.gender, "city": u.city} for u in matches]

@router.post("/like/{user_id}")
def like_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    existing = db.query(models.Like).filter(
        models.Like.liker_id == current_user.id,
        models.Like.liked_id == user_id
    ).first()

    if existing:
        return {"message": "Уже лайкнул"}

    like = models.Like(liker_id=current_user.id, liked_id=user_id)
    db.add(like)
    db.commit()

    # Проверить взаимный лайк
    mutual = db.query(models.Like).filter(
        models.Like.liker_id == user_id,
        models.Like.liked_id == current_user.id
    ).first()

    if mutual:
        return {"message": "Взаимный лайк! Это Cool! 🎉"}

    return {"message": "Лайк отправлен!"}
