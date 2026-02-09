from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma


CHROMA_PATH = "backend/rag/vectorstore"


# ---------- Load Vector DB ----------
def get_retriever():

    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )

    db = Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=embeddings
    )

    return db


# ---------- Retrieve Context ----------
def retrieve_context(query, k=3):

    db = get_retriever()

    docs = db.similarity_search(query, k=k)

    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    return context
