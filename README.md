# 🧠 EstateGenius – Real Estate AI Chatbot (RAG System)

**EstateGenius** is an intelligent **Real Estate Assistant** powered by **FastAPI**, **LangChain**, **Pinecone**, and **Gemini (Google Generative AI)**.
It helps users get real estate insights directly from uploaded PDFs — with authentication, admin dashboard, and JWT-based role management.

---

## 🚀 Features

✅ Role-based Authentication (Admin & User)
✅ Secure JWT Access + Refresh Tokens
✅ Admin Dashboard for PDF Upload
✅ Automatic Document Processing (Chunking + Embedding)
✅ Conversational Retrieval-Augmented Generation (RAG)
✅ Persistent Pinecone Vector Store
✅ Database-backed Memory-enabled Conversations
✅ Professionally formatted AI responses for real estate insights

---

## 🧩 Tech Stack

| Layer                    | Technology                     |
| ------------------------ | ------------------------------ |
| **Backend**              | FastAPI                        |
| **LLM / AI**             | LangChain + Google Gemini      |
| **Vector Store**         | Pinecone                       |
| **Embeddings**           | HuggingFace (all-MiniLM-L6-v2) |
| **Auth**                 | JWT (Access + Refresh)         |
| **Database**             | PostgreSQL                     |
| **Frontend (Templates)** | HTML (Jinja2 Templates)        |

---

## ⚙️ Setup Guide

### 1. Clone the Repository

```bash
git clone https://github.com/umair741/rag_chatbot.git
cd rag_chatbot
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate     # On Windows
# source venv/bin/activate  # On Mac/Linux
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Create `.env` File

In the root directory, add:

```
# --- API Keys ---
GOOGLE_API_KEY=your_google_gemini_api_key_here
PINECONE_API_KEY=your_pinecone_api_key_here
PINECONE_INDEX_NAME=your_pinecone_index_name_here

# --- Database ---
DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/Dataforrag
# If using Supabase, replace with your Supabase Postgres connection string.

# --- Admin Credentials ---
ADMIN_NAME=Admin
ADMIN_EMAIL=admin@gmail.com
ADMIN_PASSWORD=StrongP@ssw0rd!

# --- JWT Settings ---
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=300
REFRESH_TOKEN_EXPIRE_DAYS=7
```

### 5. Initialize Database

Make sure PostgreSQL is running, then create tables:

```bash
python db.py
```

You can also manually create an admin using:

```bash
python create_admin.py
```

---

## 🧠 Run the Application

### 1. Start FastAPI Server

```bash
uvicorn main:app --reload
```

Server will start at:
👉 [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 🧱 Folder Structure

```
rag_chatbot/
│
├── main.py                # FastAPI app (routes + auth)
├── chain.py               # LangChain RAG logic
├── processing.py          # PDF processing & embeddings
├── db.py                  # Database configuration
├── models.py              # SQLAlchemy models
├── schema.py              # Pydantic schemas
├── token_logic.py         # JWT creation & verification
├── create_admin.py        # Script to create admin user
│
├── templates/
│   ├── login.html
│   ├── signup.html
│   ├── dashboard.html
│   ├── admin.html
│
├── books/english/         # Folder for uploaded PDFs
├── .env                   # Environment variables (ignored by Git)
├── requirements.txt
└── README.md
```

---

## 🔐 Authentication Flow

1. **Signup** – Creates a normal user
2. **Login** – Returns JWT tokens (access + refresh)
3. **Admin** – Can upload new PDFs and trigger embedding
4. **User** – Can query the chatbot via `/ask`

---

## 🧾 API Routes Overview

| Method | Route               | Description               | Auth          |
| ------ | ------------------- | ------------------------- | ------------- |
| `POST` | `/signup`           | Register new user         | ❌             |
| `POST` | `/login`            | Login user (returns JWTs) | ❌             |
| `POST` | `/logout`           | Clear session             | ✅             |
| `POST` | `/refresh`          | Refresh access token      | ✅             |
| `POST` | `/admin/upload-pdf` | Upload new PDFs           | 🔒 Admin only |
| `POST` | `/ask`              | Ask chatbot questions     | ✅ User        |
| `GET`  | `/dashboard`        | User dashboard            | ✅ User        |
| `GET`  | `/admin`            | Admin dashboard           | 🔒 Admin      |

---

## 💬 Example Chat (CLI mode)

```bash
python chain.py
```

```
🤖 Chatbot CLI
You: Hi
Bot: Hi, I'm EstateGenius, your intelligent real estate assistant. How can I help you today?
```

---

## 🧠 Example Admin Workflow

1. Login as admin
2. Upload PDF files via `/admin/upload-pdf`
3. PDFs are processed → chunks → embeddings stored in Pinecone
4. Ask questions → Bot answers using document context

---

## 🧰 Example Question

```
Q: What is the average rental yield in Green Valley?
```

**Bot:**

```
📍 Green Valley Market Overview

• Average rental yield: 5.2% annually  
• Popular property types: 3-4 bedroom homes  
• Price range: $350,000 – $500,000

This area offers stable returns and consistent appreciation trends.
```

---

## 🧤 Security Notes

* `.env` is excluded from Git (`.gitignore`)
* Never commit API keys or passwords
* Rotate your JWT secret periodically
* Restrict `/admin` access properly

---

## 🧑‍💻 Author

**Umair Memon**
AI Developer & Automation Specialist
🔗 [GitHub](https://github.com/umair741)
💼 [Fiverr](https://www.fiverr.com/)

---

## 🪄 License

MIT License © 2025 Umair Memon
Free to use, modify, and distribute.

---
