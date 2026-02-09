# backend/ingestion/update_global_docs.py

from loader import load_pdf
from splitter import split_into_chunks
from vectordb import vector_db

files = [
    "backend\rag\docs\IV DELTA DATABASE  modified.pdf",
    "backend\rag\docs\Dinesh_Resume (2).pdf",
    "backend\rag\docs\Brand Book - Pi Dot.pdf"
]

docs = load_pdf(files)
chunks = split_into_chunks(docs)


vector_db.add_documents(chunks)
vector_db.persist()

print("Global docs updated ✅")
