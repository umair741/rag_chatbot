from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from fastapi import BackgroundTasks
from processing import process_all_pdfs
from chain import ask_question

app = FastAPI()

# CORS: Allow frontend to call backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Later restrict this to your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Template system
templates = Jinja2Templates(directory="templates")

# Input model for /ask route
class Question(BaseModel):
    question: str

# Serve HTML frontend
@app.get("/")
async def serve_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Process PDFs
@app.post("/process")
def process(background_tasks: BackgroundTasks):
    try:
        background_tasks.add_task(process_all_pdfs)
        return {"message": "PDF documents processed and stored."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Handle question asking
@app.post("/ask")
def ask(question: Question):
    try:
        response = ask_question(question.question)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
