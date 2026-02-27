
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import get_db, engine
import models
from auth import verify_password, create_access_token, hash_password
from routers import users, search, chat

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Dating Site 💕")
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(users.router)
app.include_router(search.router)
app.include_router(chat.router)

@app.get("/", response_class=HTMLResponse)
async def home():
    with open("templates/index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@app.get("/register", response_class=HTMLResponse)
async def register_page():
    with open("templates/register.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@app.get("/safety", response_class=HTMLResponse)
async def safety_page():
    with open("templates/safety.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@app.get("/about", response_class=HTMLResponse)
async def about_page():
    with open("templates/about.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@app.get("/premium", response_class=HTMLResponse)
async def premium_page():
    with open("templates/premium.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@app.post("/register")
def register(email: str, username: str, password: str, name: str, age: int, gender: str, city: str, db: Session = Depends(get_db)):
    if db.query(models.User).filter(models.User.email == email).first():
        raise HTTPException(status_code=400, detail="Email уже занят")
    if db.query(models.User).filter(models.User.username == username).first():
        raise HTTPException(status_code=400, detail="Username уже занят")
    user = models.User(
        email=email, username=username,
        hashed_password=hash_password(password),
        name=name, age=age, gender=gender, city=city
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": "Аккаунт создан!", "user_id": user.id}

@app.get("/login", response_class=HTMLResponse)
async def login_page():
    with open("templates/login.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard_page():
    with open("templates/dashboard.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@app.get("/profile", response_class=HTMLResponse)
async def profile_page():
    with open("templates/profile.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@app.get("/chat", response_class=HTMLResponse)
async def chat_page():
    with open("templates/chat.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())


@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Неверный логин или пароль")
    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}