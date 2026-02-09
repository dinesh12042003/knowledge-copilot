from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma



# ---------- Config ----------
CHROMA_PATH = "backend/rag/vectorstore"


# ---------- Load & Process ----------
def ingest_pdf(file_path):

    # 1️⃣ Load PDF
    loader = PyPDFLoader(file_path)
    documents = loader.load()

    # 2️⃣ Split into chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100
    )

    chunks = splitter.split_documents(documents)

    # 3️⃣ Create embeddings
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )

    # 4️⃣ Store in vector DB
    db = Chroma.from_documents(
        chunks,
        embeddings,
        persist_directory=CHROMA_PATH
    )

    db.persist()

    return len(chunks)
