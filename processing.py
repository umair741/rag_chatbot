import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

load_dotenv()

PDF_DIR = "books/english"
persist_directory = "chroma_db"
embedding_function = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")


def get_pdf_paths(folder):
    return [os.path.join(folder, f) for f in os.listdir(folder) if f.lower().endswith(".pdf")]


def extract_documents(file_path):
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    filename = os.path.basename(file_path)
    for i, doc in enumerate(documents):
        doc.metadata["filename"] = filename
        doc.metadata["page"] = i + 1
    return documents


def split_documents(documents, chunk_size=1000, chunk_overlap=100):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", " ", ""],
        keep_separator=True
    )
    split_docs = splitter.split_documents(documents)
    for idx, chunk in enumerate(split_docs):
        chunk.metadata["chunk_id"] = f"{chunk.metadata.get('filename', 'file')}_chunk_{idx}"
    return split_docs


def create_embeddings(chunks):
    texts, filtered_chunks = [], []
    for doc in chunks:
        content = doc.page_content.strip()
        if content:
            texts.append(content)
            filtered_chunks.append(doc)
    embeddings = embedding_function.embed_documents(texts)
    return filtered_chunks, embeddings


def store_embeddings(chunks, embeddings):
    os.makedirs(persist_directory, exist_ok=True)
    db = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_function,
        persist_directory=persist_directory
    )
    db.persist()


def process_all_pdfs():
    if not os.path.exists(PDF_DIR):
        raise FileNotFoundError(f"PDF folder not found: {PDF_DIR}")

    pdf_paths = get_pdf_paths(PDF_DIR)
    if not pdf_paths:
        raise ValueError("No PDF files found.")

    all_chunks = []
    for path in pdf_paths:
        docs = extract_documents(path)
        chunks = split_documents(docs)
        all_chunks.extend(chunks)

    if not all_chunks:
        raise ValueError("No content chunks generated.")

    filtered_chunks, embeddings = create_embeddings(all_chunks)
    store_embeddings(filtered_chunks, embeddings)

if __name__ == "__main__":
    process_all_pdfs()
