import base64
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS

def process_pdf(file_path):
    loader = PyPDFLoader(file_path)
    pages = loader.load_and_split()
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    db = FAISS.from_documents(pages, embeddings)
    return db

def generate_answer(query, db, llm):
    docs = db.similarity_search(query)
    relevant_search = "\n".join([x.page_content for x in docs])
    gemini_prompt = ("Use the following pieces of context to answer the question. "
                      "If you don't know the answer, just say you don't know the answer. Don't make it up.")
    input_prompt = f"{gemini_prompt}\nContext: {relevant_search}\nUser Question: {query}"
    result = llm.invoke(input_prompt)
    return result.content