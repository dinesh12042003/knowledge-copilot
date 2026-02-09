# backend/rag/ingest_global.py
from pathlib import Path
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader

# -----------------------------
# Paths & Embeddings
# -----------------------------
CHROMA_PATH = Path(__file__).parent / "vectorstore" / "global"
CHROMA_PATH.mkdir(parents=True, exist_ok=True)  # ensure directory exists

# HuggingFace embeddings model
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")


# -----------------------------
# Function: Get or Create Global Vectorstore
# -----------------------------
def get_global_vectorstore():
    """
    Returns the Chroma vectorstore for global documents.
    Creates a new one if it doesn't exist yet.
    """
    db = Chroma(
        persist_directory=str(CHROMA_PATH),
        embedding_function=embeddings
    )
    return db


# -----------------------------
# Function: Ingest Global PDF
# -----------------------------
def ingest_global_pdf(pdf_path: str):
    """
    Loads a PDF, adds metadata, and indexes it into the global vectorstore.
    
    Args:
        pdf_path: str, path to PDF file
    """
    pdf_path = Path(pdf_path)
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found at {pdf_path}")

    loader = PyPDFLoader(str(pdf_path))
    pages = loader.load()

    # Add metadata
    for p in pages:
        p.metadata["scope"] = "global"
        p.metadata["source"] = str(pdf_path)

    # Get global vectorstore
    db = get_global_vectorstore()
    db.add_documents(pages)
    # db.persist()

    print(f"Global PDF indexed ✔: {pdf_path.name}")


# -----------------------------
# Optional: Ingest all PDFs in folder
# -----------------------------
def ingest_all_global_pdfs(folder_path: str):
    folder_path = Path(folder_path)
    if not folder_path.exists():
        raise FileNotFoundError(f"Folder not found: {folder_path}")

    pdfs = list(folder_path.glob("*.pdf"))
    for pdf in pdfs:
        ingest_global_pdf(str(pdf))
