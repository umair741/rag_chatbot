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
        output_key="answer",
        k=10  # Keep only last 10 exchanges
    )

  # Custom prompt template
    custom_prompt = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(
                """You are a helpful AI assistant. 
    -if user is greeting with ALways reply with Hi, I’m Umair, your assistant. How can I assist you today
    - Use only the context provided from relevant documents to answer questions. 
    - Answer concisely and accurately. 
    - Do NOT greet the user unless the user explicitly asks for a greeting. 
    - If the answer is not in the context, say "I don't know" or "The information is not available."
    - Stay on topic and do not add extra commentary.
    "

    Context:
    {context}"""
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


qa_chain = load_chatbot()


def ask_question(question: str) -> dict:

    result = qa_chain.invoke({"question": question})

    return {"answer": result["answer"]}



if __name__ == "__main__":
    print("🤖 Chatbot CLI")
    while True:
        q = input("You: ")
        if q.lower() == "exit":
            break
        print("Bot:", ask_question(q))
