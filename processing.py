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
    files = os.listdir(folder)            
    pdf_files = []                          

    for f in files:
        if f.lower().endswith(".pdf"):      
            pdf_files.append(os.path.join(folder, f))  

    return pdf_files


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

def filter_empty_chunks(chunks):
    return [doc for doc in chunks if doc.page_content.strip()]



def store_embeddings(chunks): 
    os.makedirs(persist_directory, exist_ok=True)
    db = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_function,
        persist_directory=persist_directory
    )

def process_pdf_batch(pdf_paths_batch):

    batch_chunks = []
    failed_files=[]
    
    for path in pdf_paths_batch:
        try:
            docs = extract_documents(path)
            chunks = split_documents(docs)
            batch_chunks.extend(chunks)
        except Exception as e:
            filename=os.path.basename(path)
            print(f"❌ Error processing {filename}: {str(e)}")
            failed_files.append(filename)
            
            continue  
          
    if failed_files:
        print(f"⚠️  Failed files in this batch: {len(failed_files)}")
    
    return batch_chunks
        
        
def process_all_pdfs():
    if not os.path.exists(PDF_DIR):
        raise FileNotFoundError(f"PDF folder not found: {PDF_DIR}")

    pdf_paths = get_pdf_paths(PDF_DIR)

    if not pdf_paths:
        raise ValueError("No PDF files found.")
    
        
    print(f"📁 Total PDFs: {len(pdf_paths)}")
    
    batch_size = 10
    
    # Har batch ko process karo
    for i in range(0, len(pdf_paths), batch_size):
        batch = pdf_paths[i:i + batch_size]
        
        # Batch process
        batch_chunks = process_pdf_batch(batch)
        
        # Filter aur save
        if batch_chunks:
            filtered_chunks = filter_empty_chunks(batch_chunks)
            store_embeddings(filtered_chunks)
            print(f"✅ Batch {i//batch_size + 1}: {len(filtered_chunks)} chunks")
    
    print("🎉 All done!")
    


if __name__ == "__main__":
    process_all_pdfs()
