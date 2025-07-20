RAG Chatbot with Gemini, FastAPI, LangChain, and ChromaDB
This project is a Retrieval-Augmented Generation (RAG) chatbot that processes PDF documents, stores their embeddings in ChromaDB, and generates context-aware responses using Google's Gemini API, LangChain, and FastAPI. The chatbot retrieves relevant information from a vectorized knowledge base of PDF documents and supports interaction via a command-line interface (CLI), a FastAPI-based API, or a basic web UI. PDF documents must be manually placed in the books/english folder, as the project does not include a file upload UI.
Tech Stack

Python 3.10: Core programming language.
FastAPI: Asynchronous web framework for the API.
LangChain: Framework for managing the RAG pipeline, document processing, and conversational workflows.
Google Gemini API (gemini-2.0-flash): Large language model for response generation.
HuggingFace Embeddings (all-MiniLM-L6-v2): For creating document embeddings.
ChromaDB: Persistent vector database for storing embeddings.
PyPDF: Library for extracting text from PDFs.
Uvicorn: ASGI server for running the FastAPI application.
python-dotenv: For loading environment variables from a .env file.
Jinja2: Template engine for rendering the basic web UI in the templates folder.

Features

PDF Processing: Extracts text from PDFs in the books/english folder.
RAG Pipeline: Combines document retrieval with generative responses.
ChromaDB Vector Store: Persists embeddings for efficient similarity searches.
Conversational Memory: Maintains chat history for context-aware responses.
FastAPI Backend: Provides a scalable API.
CLI Interface: Allows testing via command-line.
Basic Web UI: Simple web interface in the templates folder (no file upload functionality).
Manual PDF Placement: Requires PDFs to be manually placed in books/english.

Prerequisites

Python 3.9 or higher
Google Cloud account with a Gemini API key
Git (optional, for cloning the repository)
PDF documents in the books/english folder
A .env file with your Gemini API key (see Setup Environment Variables below)

Installation and Running the Project

Clone the RepositoryClone the project from GitHub and navigate to the project directory:
git clone https://github.com/your-username/your-repo.git
cd your-repo


Set Up a Virtual EnvironmentCreate and activate a virtual environment to isolate dependencies:
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


Install DependenciesThe project includes a requirements.txt file with all necessary dependencies. Install them using:
pip install -r requirements.txt


Setup Environment VariablesYou must create a .env file in the project root to store your Gemini API key, which is required for the Google Gemini API. Add the following line to the .env file:

GOOGLE_API_KEY=your_google_api_key

Replace your_google_api_key with your actual API key from Google AI Studio. Ensure the .env file is not committed to version control (e.g., add it to .gitignore).

Prepare PDF DocumentsPlace your PDF files in the books/english folder. The project does not include a file upload UI, so PDFs must be manually added to this folder for processing.


Running the Project

Process PDFsProcess the PDFs in books/english to extract text, generate embeddings, and store them in ChromaDB:
python process_pdfs.py

This creates embeddings and persists them in the chroma_db directory.

Run the API and Web UIStart the FastAPI server to enable the API and basic web UI:
uvicorn main:app --reload


API: Available at http://localhost:8000.
Web UI: Access the basic UI (if configured) at http://localhost:8000 (e.g., / or /chat).


Interact via APISend POST requests to the /chat endpoint using curl, Postman, or a custom frontend:
curl -X POST "http://localhost:8000/chat" -H "Content-Type: application/json" -d '{"message": "What is RAG?"}'

Responses include the answer and source metadata (e.g., filename and page number).

Interact via Web UIOpen a browser and navigate to http://localhost:8000 to use the basic web UI from the templates folder. Enter queries to receive responses. Note: You cannot upload PDFs via the UI; place them in books/english manually.

Interact via CLIRun the CLI for command-line interaction:
python chatbot.py

Type questions to get responses with source metadata. Type exit to quit.


Project Structure
your-repo/
├── books/
│   └── english/          # Folder for PDF documents (manually place PDFs here)
├── chroma_db/            # ChromaDB persistence directory
├── templates/            # Folder for basic web UI templates
├── main.py               # FastAPI application for API and web UI
├── processing.py         # Script to process PDFs and store embeddings
├── chain.py              # RAG pipeline and conversational logic
├── .env                  # Environment variables (must be created)
├── requirements.txt      # Dependencies (included in project)
└── README.md             # This file

Extending the Project

File Upload UI: Add file upload functionality to the web UI to place PDFs in books/english.
Persistent Storage: Use a hosted Chroma instance or FAISS/Pinecone for scalability.
Enhanced UI: Upgrade the web UI with Streamlit or React.
Advanced Retrieval: Implement hybrid search or re-ranking.
Authentication: Add API key or OAuth for secure access.
Custom Prompts: Modify the prompt template for domain-specific responses.

Troubleshooting

Missing .env File: Ensure the .env file has a valid GOOGLE_API_KEY.
Dependency Issues: Run pip install -r requirements.txt to ensure all dependencies are installed.
ChromaDB Issues: Verify the chroma_db folder is writable and embeddings are generated.
PDF Processing: Ensure valid PDFs are in books/english. No file upload is available.
Web UI Issues: Check that templates in the templates folder are correctly configured.

Contributing
Contributions are welcome! Open an issue or submit a pull request on GitHub.
License
This project is licensed under the MIT License.
