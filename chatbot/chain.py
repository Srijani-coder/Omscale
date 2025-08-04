from langchain_openai import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain_community.vectorstores import FAISS
from chatbot.loader import load_documents
import os
from dotenv import load_dotenv
load_dotenv()

retriever = load_documents('./data/law_docs/')
api_key = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(openai_api_key = api_key, temperature=0)

qa_chain = ConversationalRetrievalChain.from_llm(
    llm,
    retriever.as_retriever(),
    return_source_documents=True
)

def get_bot_response(query):
    result = qa_chain({"question": query, "chat_history": []})
    return result['answer']
