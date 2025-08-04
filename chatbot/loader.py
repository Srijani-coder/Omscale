from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
#from langchain_community.embeddings.openai import OpenAIEmbeddings
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
from langchain_openai import *
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
models = client.models.list()

for m in models.data:
    print(m.id)

def load_documents(path):
    loader = DirectoryLoader(path, glob='*.pdf', loader_cls=PyPDFLoader)
    docs = loader.load()
    if not docs:
        raise ValueError("No documents found. Please add PDFs files to data/law_docs/")
    
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    split_docs = splitter.split_documents(docs)

    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
    vectorstore = FAISS.from_documents(split_docs, embeddings)
    return vectorstore
