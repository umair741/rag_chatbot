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
            """You are a helpful and concise AI assistant always reply greeting with hi hello how r u how can i assit you today. 
    Use the context provided below from relevant documents to answer the user's question accurately.
    - Only use the information present in the context.
    - Do not make up answers.
    - Keep your answers short and to the point.
    - If the answer is not found in the context, politely say "I don't know" or "The information is not available."

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
