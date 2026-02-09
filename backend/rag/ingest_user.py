# backend/rag/ingest_user.py

from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from backend.rag.vectorstore.vectorstore import get_vectorstore

# -----------------------------
# Base path where user vectorstores are stored
# -----------------------------
USER_VECTORSTORE_PATH = Path(__file__).parent / "vectorstore" / "users"
USER_VECTORSTORE_PATH.mkdir(parents=True, exist_ok=True)

# Embeddings model
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")


# -----------------------------
# Function: Get or Create User Vectorstore
# -----------------------------
def get_user_vectorstore(user_id: str):
    """
    Returns a Chroma vectorstore for a specific user.
    If the user has no uploaded documents, creates a new vectorstore.
    """
    user_path = USER_VECTORSTORE_PATH / user_id
    user_path.mkdir(parents=True, exist_ok=True)  # ensure folder exists

    db = Chroma(
        persist_directory=str(user_path),
        embedding_function=embeddings
    )

    # If vectorstore is empty, return None so RAG can skip user docs
    if not db._collection.count():  # _collection is internal Chroma collection
        return None

    return db


# -----------------------------
# Function: Ingest User PDF
# -----------------------------
def ingest_user_pdf(pdf_path: str, user_id: str):
    """
    Loads a user PDF, adds metadata, and indexes it into the user's vectorstore.

    Args:
        pdf_path: str, path to PDF file
        user_id: str, Google ID or unique user identifier
    """
    pdf_path = Path(pdf_path)
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found at {pdf_path}")

    loader = PyPDFLoader(str(pdf_path))
    pages = loader.load()

    # Add metadata
    for p in pages:
        p.metadata["scope"] = "user"
        p.metadata["user_id"] = user_id
        p.metadata["source"] = str(pdf_path)

    # Get user vectorstore
    db = get_vectorstore(persist_dir=USER_VECTORSTORE_PATH / user_id)
    db.add_documents(pages)
    db.persist()

    print(f"User PDF indexed ✔: {pdf_path.name} for user {user_id}")
