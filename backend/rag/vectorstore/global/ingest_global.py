from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from pathlib import Path

DOCS_PATH = Path(__file__).parent / "docs"
VECTORSTORE_PATH = Path(__file__).parent / "vectorstore" / "global"

# 1️⃣ Load all PDFs
documents = []
for pdf_file in DOCS_PATH.glob("*.pdf"):
    loader = PyPDFLoader(str(pdf_file))
    docs = loader.load()
    documents.extend(docs)

# 2️⃣ Split into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)
docs_split = text_splitter.split_documents(documents)

# 3️⃣ Embeddings
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# 4️⃣ Create Chroma vectorstore
VECTORSTORE_PATH.mkdir(parents=True, exist_ok=True)
db = Chroma.from_documents(
    docs_split,
    embedding=embeddings,
    persist_directory=str(VECTORSTORE_PATH)
)
db.persist()
print("✅ Global vectorstore created!")
