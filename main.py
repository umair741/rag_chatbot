from fastapi import FastAPI, Depends, HTTPException, Request, BackgroundTasks, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse, RedirectResponse
from sqlalchemy.orm import Session
from db import get_db
import models, schema
from security import hash_password, verify_password
from token_logic import create_access_token, create_refresh_token, verify_token, admin_required
from processing import process_all_pdfs
from chain import ask_question
from schema import Question
import os
import jwt
from token_logic import SECRET_KEY, ALGORITHM

# PDF folder
PDF_DIR = "books/english"
os.makedirs(PDF_DIR, exist_ok=True)

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Templates
templates = Jinja2Templates(directory="templates")

# ----------------------
# HTML Routes
# ----------------------
@app.get("/")
async def serve_index(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/login")
async def serve_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/signup")
async def serve_signup(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@app.get("/dashboard")
def serve_dashboard(request: Request, current_user: dict = Depends(verify_token)):
    """Protected route - requires valid JWT token"""
    return templates.TemplateResponse("dashboard.html", {"request": request, "user": current_user})

@app.get("/admin")
def serve_admin(request: Request, current_user: dict = Depends(admin_required)):
    """Protected admin route - requires admin role"""
    return templates.TemplateResponse("admin.html", {"request": request, "user": current_user})

# ----------------------
# Auth Routes
# ----------------------
@app.post("/signup", response_model=schema.UserResponse)
def signup(user: schema.UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_pw = hash_password(user.password)
    new_user = models.User(name=user.name, email=user.email, password=hashed_pw, role="user")
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/login")
def login(user: schema.UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    token_data = {"user_id": db_user.id, "email": db_user.email, "role": db_user.role}
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)

    response = JSONResponse({
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user_id": db_user.id,
        "name": db_user.name,
        "role": db_user.role
    })

    # Set cookie for browser
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=60 * 60 * 5,  # 5 hours
        samesite="lax"
    )
    return response

@app.post("/logout")
def logout():
    """Clear authentication cookie"""
    response = JSONResponse({"message": "Logged out successfully"})
    response.delete_cookie("access_token")
    return response

@app.post("/refresh")
def refresh_token_endpoint(refresh_token: str):
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Refresh token expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    new_access_token = create_access_token({
        "user_id": payload["user_id"],
        "email": payload["email"],
        "role": payload["role"]
    })

    return {"access_token": new_access_token, "token_type": "bearer"}

# ----------------------
# Admin Routes
# ----------------------
@app.post("/admin/upload-pdf")
def upload_pdf(
    file: UploadFile = File(...),
    background_tasks: BackgroundTasks = None,
    current_user: dict = Depends(admin_required)
):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    save_path = os.path.join(PDF_DIR, file.filename)
    with open(save_path, "wb") as f:
        f.write(file.file.read())

    background_tasks.add_task(process_all_pdfs)  # process all PDFs

    return {"message": f"PDF '{file.filename}' uploaded to '{PDF_DIR}' and processing started."}

# ----------------------
# Chat / Ask Route
# ----------------------
@app.post("/ask")
def ask(question: Question, current_user: dict = Depends(verify_token)):
    """Protected route - requires authentication"""
    response = ask_question(question.question)
    return response