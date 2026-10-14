import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import TextLoader
import logging

load_dotenv()
API_KEY=os.getenv("GROQ_API_KEY")

persist_directory = "./icici_DB"
data_folder="resources/"

os.makedirs(persist_directory, exist_ok=True)

doc=[]
for file in os.listdir(data_folder):
    if file.endswith('.pdf'):
        file_path=os.path.join(data_folder,file)
    loader = TextLoader(file_path,encoding="utf-8")
    documents=loader.load()
    doc.extend(documents)
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
chunks = text_splitter.split_documents(doc)
embedding=HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
vector_db=Chroma(embedding_function=embedding,persist_directory=persist_directory)
vector_db.add_documents(chunks)

        
def rag_tool(question):

    retriever=vector_db.similarity_search(question, k=4)
    response = "\n".join([doc.page_content for doc in retriever])

    # prompt = f"""
    # - you are icici bank customer support assistant.
    # - you must answer the retrieved context provided below.
    # - you are following the below rules.

    # RULES:

    # 1. Use ONLY the retrieved context.
    # 2. Do NOT use external knowledge.
    # 3. Do NOT guess, assume, or infer missing details.
    # 4. If the question is NOT related to ICICI Bank services then response:
    #     “I can help with ICICI Bank services and banking questions. Please ask a related questions.”
    # 5. Keep the answer short, precise and complete.
    # 6. Do NOT add explanations, summaries, or extra information.

    # question:{question}  
    # context:{context}
    # Answer:
    # """



    # llm = ChatGroq(
    #         model="openai/gpt-oss-120b",
    #         api_key=API_KEY,
    #     )
    
    # response=llm.invoke(prompt)
    # logging.debug("response generated")
    # docs = context.invoke(question)
    # response="\n\n".join([doc.page_content for doc in docs])
    return response









