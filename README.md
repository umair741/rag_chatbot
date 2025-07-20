# RAG Chatbot with Gemini, FastAPI, LangChain, and ChromaDB

This project is a Retrieval-Augmented Generation (RAG) chatbot that processes PDF documents, stores their embeddings in ChromaDB, and generates context-aware responses using Google's Gemini API, LangChain, and FastAPI. The chatbot retrieves relevant information from a vectorized knowledge base of PDF documents and supports interaction via a command-line interface (CLI), a FastAPI-based API, or a basic web UI. **PDF documents must be manually placed in the `books/english` folder**, as the project does not include a file upload UI.

---

## 💡 Tech Stack

* **Python 3.10**: Core programming language
* **FastAPI**: Asynchronous web framework for the API
* **LangChain**: Framework for managing the RAG pipeline and workflows
* **Google Gemini API (`gemini-2.0-flash`)**: For response generation
* **HuggingFace Embeddings (`all-MiniLM-L6-v2`)**: For creating document embeddings
* **ChromaDB**: Persistent vector database
* **PyPDF**: For PDF text extraction
* **Uvicorn**: ASGI server for FastAPI
* **python-dotenv**: Environment variable loader
* **Jinja2**: For basic HTML templates (web UI)

---

## 🌟 Features

* 📄 **PDF Processing**: Extracts text from PDFs in `books/english`
* 💡 **RAG Pipeline**: Combines document retrieval with LLM generation
* 📊 **ChromaDB Vector Store**: Efficient similarity search
* ⚖️ **Conversational Memory**: Maintains history for context
* 🚀 **FastAPI Backend**: RESTful and async
* ⌨️ **CLI Support**: Ask questions from terminal
* 📃 **Web UI**: Basic HTML-based interface (no file upload)

---

## ✅ Prerequisites

* Python 3.9 or higher
* Google Cloud account with Gemini API key
* PDF documents in the `books/english` folder
* `.env` file with your Gemini API key (see below)

---

## 🚧 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

### 2. Create a Virtual Environment

```bash
python -m venv venv

# Activate
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the root with your Gemini API key:

```env
GOOGLE_API_KEY=your_google_api_key
```

---

## 📚 Add Your Documents

> **No file upload UI is provided.** You must manually add your `.pdf` files into:

```
books/english/
```

---

## 🚀 Running the Project

### Step 1: Process PDFs

```bash
python processing.py
```

This extracts text, generates embeddings, and stores them in `chroma_db/`

### Step 2: Start the API

```bash
uvicorn main:app --reload
```

* API: [http://localhost:8000/docs](http://localhost:8000/docs)
* Web UI: [http://localhost:8000/](http://localhost:8000/)

---

## 🎧 Interact with the Bot

### 🛠️ Via API

```bash
curl -X POST "http://localhost:8000/chat" \
-H "Content-Type: application/json" \
-d '{"message": "What is RAG?"}'
```

### 🌐 Via Web UI

Go to: [http://localhost:8000/](http://localhost:8000/)
(Type your question in the simple UI)

### ⌨️ Via CLI

```bash
python chatbot.py
```

Type your questions directly in the terminal. Type `exit` to quit.

---

## 🗄️ Project Structure

```
your-repo/
├── books/
│   └── english/          # Place your PDFs here manually
├── chroma_db/            # Chroma persistence folder
├── templates/            # HTML templates (basic UI)
├── main.py               # FastAPI application
├── processing.py         # PDF embedding logic
├── chain.py              # RAG + Gemini pipeline  
├── .env                  # Contains GOOGLE_API_KEY
├── requirements.txt      # Required packages
└── README.md             # This file
```

---

## 🔧 Extending the Project

* 📂 **Add File Upload UI** to auto-place PDFs in `books/english`
* 📊 **Switch to Hosted Chroma**, Pinecone, or FAISS for large-scale use
* 🚀 **Upgrade UI** with Streamlit or React frontend
* 🤖 **Auth Layer** with tokens or OAuth
* 🌍 **Custom Prompt Templates** for domain-specific use cases

---

## ⚠️ Troubleshooting

* **Missing `.env`**: Make sure `GOOGLE_API_KEY` is set
* **PDF Not Processed**: Ensure your files are in `books/english` and rerun `processing.py`
* **Web UI Not Loading**: Check `templates/` folder exists
* **Embedding Errors**: Make sure your HuggingFace model and ChromaDB are installed properly

---

## 🌟 Author

Built by **Umair Memon**
GitHub: [umair741](https://github.com/umair741)
Email: [umics38@gmail.com](mailto:umics38@gmail.com)

---

## 📄 License

This project is licensed under the **MIT License**.
