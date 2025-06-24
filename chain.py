import os
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain.chains import ConversationalRetrievalChain

load_dotenv()

embedding_function = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
persist_directory = "chroma_db"

def load_chatbot():
    db = Chroma(persist_directory=persist_directory, embedding_function=embedding_function)
    retriever = db.as_retriever()

    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        output_key="answer"
    )

    # Custom prompt template
    custom_prompt = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(
            "You are a helpful assistant. Use the provided context and conversation history to answer the user's question clearly.\n{context}"
        ),
        HumanMessagePromptTemplate.from_template("{question}")
    ])

    # Gemini model with fix for SystemMessage
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        temperature=0.3,
        convert_system_message_to_human=True  
    )

    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        return_source_documents=True,
        combine_docs_chain_kwargs={"prompt": custom_prompt},
        verbose=True
    )
    return qa_chain
def ask_question(question: str) -> dict:
    chain = load_chatbot()
    result = chain.invoke({"question": question})

    sources = []
    for doc in result.get("source_documents", []):
        sources.append({
            "filename": doc.metadata.get("filename", "Unknown"),
            "page": doc.metadata.get("page", "N/A")
        })

    return {
        "answer": result["answer"],
        "sources": sources
    }


if __name__ == "__main__":
    print("🤖 Chatbot CLI")
    while True:
        q = input("You: ")
        if q.lower() == "exit":
            break
        print("Bot:", ask_question(q))
