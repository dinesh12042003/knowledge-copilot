from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from pathlib import Path

# Path to your Chroma DB folder
CHROMA_PATH = Path(__file__).parent / "vectorstore"

def get_vectorstore():
    """
    Returns a Chroma vector store instance with embeddings
    """
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )

    db = Chroma(
        persist_directory=str(CHROMA_PATH),
        embedding_function=embeddings
    )

    return db
