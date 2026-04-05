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

# ===== PWA =====
PWA_TAGS = """
<link rel="manifest" href="/manifest.json">
<meta name="theme-color" content="#ff4d6d">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="Zhanym">
<link rel="apple-touch-icon" href="/static/icons/icon-192.png">
<script>if('serviceWorker' in navigator){navigator.serviceWorker.register('/sw.js');}</script>
"""

def render(filename):
    with open(f"templates/{filename}", "r", encoding="utf-8") as f:
        content = f.read()
    return HTMLResponse(content.replace("</head>", PWA_TAGS + "</head>"))

@app.get("/sw.js")
async def service_worker():
    return FileResponse("static/sw.js", media_type="application/javascript")

@app.get("/manifest.json")
async def manifest():
    return FileResponse("static/manifest.json", media_type="application/json")

# ===== СТРАНИЦЫ =====
@app.get("/", response_class=HTMLResponse)
async def home():
    return render("index.html")

@app.get("/login", response_class=HTMLResponse)
async def login_page():
    return render("login.html")

@app.get("/register", response_class=HTMLResponse)
async def register_page():
    return render("register.html")

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard_page():
    return render("dashboard.html")

@app.get("/profile", response_class=HTMLResponse)
async def profile_page():
    return render("profile.html")

@app.get("/chat", response_class=HTMLResponse)
async def chat_page():
    return render("chat.html")

@app.get("/likes", response_class=HTMLResponse)
async def likes_page():
    return render("likes.html")

@app.get("/edit_profile", response_class=HTMLResponse)
async def edit_profile_page():
    return render("edit_profile.html")

@app.get("/search", response_class=HTMLResponse)
async def search_page():
    return render("search.html")

@app.get("/subscription", response_class=HTMLResponse)
async def subscription_page():
    return render("subscription.html")

@app.get("/onboarding", response_class=HTMLResponse)
async def onboarding_page():
    return render("onboarding.html")

@app.get("/premium", response_class=HTMLResponse)
async def premium_page():
    return render("premium.html")

@app.get("/safety", response_class=HTMLResponse)
async def safety_page():
    return render("safety.html")

@app.get("/about", response_class=HTMLResponse)
async def about_page():
    return render("about.html")

@app.get("/forgot-password", response_class=HTMLResponse)
async def forgot_password_page():
    return render("forgot_password.html")

@app.get("/reset-password", response_class=HTMLResponse)
async def reset_password_page():
    return render("reset_password.html")

@app.get("/profile/{user_id}", response_class=HTMLResponse)
async def user_profile_page(user_id: int):
    return render("user.html")

# ===== API =====
@app.post("/register")
def register(
    email: str, username: str, password: str, name: str,
    age: int, gender: str, city: str,
    phone: str = None, bio: str = None, height: int = None,
    zodiac: str = None, goal: str = None, sport: str = None,
    drink: str = None, smoke: str = None, pet: str = None,
    communication: str = None, love_language: str = None,
    education: str = None, interests: str = None,
    db: Session = Depends(get_db)
):
    if db.query(models.User).filter(models.User.email == email).first():
        raise HTTPException(status_code=400, detail="Email уже занят")
    if db.query(models.User).filter(models.User.username == username).first():
        raise HTTPException(status_code=400, detail="Username уже занят")
    user = models.User(
        email=email, username=username,
        hashed_password=hash_password(password),
        name=name, age=age, gender=gender, city=city,
        phone=phone, bio=bio, height=height,
        zodiac=zodiac, goal=goal, sport=sport,
        drink=drink, smoke=smoke, pet=pet,
        communication=communication, love_language=love_language,
        education=education, interests=interests
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": "Аккаунт создан!", "user_id": user.id}

@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Неверный логин или пароль")
    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}


from routers.admin_router import router as admin_router
app.include_router(admin_router)

@app.get("/admin", response_class=HTMLResponse)
async def admin_page():
    return render("admin.html")

from routers import subscriptions
app.include_router(subscriptions.router)
