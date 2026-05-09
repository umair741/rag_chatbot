import os
from dotenv import load_dotenv
from langchain_community.vectorstores import Pinecone as PineconeVectorStore
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain.chains import ConversationalRetrievalChain
from pinecone import Pinecone

load_dotenv()

embedding_function = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def load_chatbot():
    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
    index = pc.Index(os.getenv("PINECONE_INDEX_NAME"))
    
    db = PineconeVectorStore(
        index=index,
        embedding=embedding_function,
        text_key="text"
    )
    retriever = db.as_retriever()

    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        output_key="answer",
        k=10
    )

    custom_prompt = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(
            """You are EstateGenius AI Assistant - an intelligent real estate advisor specialized in property analysis, market insights, and investment guidance.

IDENTITY & GREETING:
- Your name is EstateGenius
- When user greets you (hi, hello, hey, etc.), ALWAYS respond: "Hi, I'm EstateGenius, your intelligent real estate assistant. How can I help you with properties, market analysis, or investment strategies today?"
- Only greet when user explicitly greets first
- Maintain a professional yet friendly tone

CORE RESPONSIBILITIES:
Provide expert guidance on real estate topics including:
- Property valuations and market trends
- Investment strategies and ROI analysis
- Neighborhood insights and comparisons
- Buying/selling process guidance
- Mortgage and financing information
- Property management best practices

ANSWER GUIDELINES - VERY IMPORTANT:
1. Use ONLY the context provided from relevant documents to answer questions
2. Answer in a clear, structured, and professional manner
3. If the answer is NOT in the provided context, respond: 
   "I don't have that specific information in my current knowledge base. Could you provide more details or rephrase your question?"
4. Stay strictly on topic - focus ONLY on real estate queries
5. Do NOT make up information outside the given context

RESTRICTIONS:
- Never discuss topics outside real estate domain
- Never provide financial advice requiring certification
- Always remind users to consult licensed professionals for legal/financial decisions

Context:
{context}"""
        ),
        HumanMessagePromptTemplate.from_template("{question}")
    ])

    llm = ChatGoogleGenerativeAI(
        model="gemini-3-flash-preview",
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