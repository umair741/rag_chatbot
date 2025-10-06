
# from fastapi import FastAPI, Depends
# from sqlalchemy.orm import Session
# from db import get_db
# from sqlalchemy import text
# from fastapi import FastAPI, HTTPException, Request
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.templating import Jinja2Templates
# from pydantic import BaseModel
# from fastapi import BackgroundTasks
# from processing import process_all_pdfs
# from chain import ask_question

# app = FastAPI()

# # CORS: Allow frontend to call backend
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Later restrict this to your domain
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Template system
# templates = Jinja2Templates(directory="templates")

# # Input model for /ask route
# class Question(BaseModel):
#     question: str

# # Serve HTML frontend
# @app.get("/")
# async def serve_index(request: Request):
#     return templates.TemplateResponse("index.html", {"request": request})

# # Process PDFs
# @app.post("/process")
# def process(background_tasks: BackgroundTasks):
#     try:
#         background_tasks.add_task (process_all_pdfs)
#         return {"message": "PDF documents processed and stored."}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# # Handle question asking
# @app.post("/ask")
# def ask(question: Question):
#     try:
#         response = ask_question(question.question)
#         return response
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
    



# @app.get("/test-db")
# def test_db_connection(db: Session = Depends(get_db)):
#     try:
#         result = db.execute(text("SELECT 1"))
#         return {"status": "✅ DB connected", "result": result.scalar()}
#     except Exception as e:
#         return {"status": "❌ Connection failed", "error": str(e)}


from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
import models, schema
from security import hash_password, verify_password

app = FastAPI()

# ✅ Signup Route
@app.post("/signup", response_model=schema.UserResponse)
def signup(user: schema.UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = hash_password(user.password)
    new_user = models.User(name=user.name, email=user.email, password=hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# ✅ Login Route
@app.post("/login")
def login(user: schema.UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid email or password")

    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    return {"message": "Login successful", "user_id": db_user.id, "name": db_user.name}
