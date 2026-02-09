from backend.rag.ingest_user import get_user_vectorstore  # user docs
from backend.rag.ingest_global import get_global_vectorstore  # global docs

# ----------------------------
# System Prompt / Rules
# ----------------------------
SYSTEM_PROMPT = """You are a helpful AI assistant. 
Answer questions concisely and clearly.
Always use information from the provided documents.
If the answer is not found in the documents, respond politely that you do not know."""

# ----------------------------
# Retrieve Context Function
# ----------------------------
def retrieve_context(user_query: str, user_id: str = None, k_global=3, k_user=3):
    """
    Retrieves context for a query combining:
    1. Global documents (shared PDFs)
    2. User-specific documents (uploaded by that user)
    3. Returns system prompt + combined context

    Args:
        user_query: string
        user_id: optional, string to fetch user-specific docs
        k_global: top-k global chunks
        k_user: top-k user chunks
    Returns:
        tuple:
            context_str: combined context ready to feed LLM
            sources: list of sources for reference / citation
    """

    combined_context = SYSTEM_PROMPT + "\n\n"
    sources = []

    # ----------------------------
    # 1️⃣ Global documents
    # ----------------------------
    global_db = get_global_vectorstore()
    global_docs = global_db.similarity_search(user_query, k=k_global)
    if global_docs:
        global_text = "\n\n".join([doc.page_content for doc in global_docs])
        combined_context += "Global Docs:\n" + global_text + "\n\n"
        sources.extend([doc.metadata.get("source", "global") for doc in global_docs])

    # ----------------------------
    # 2️⃣ User-specific documents
    # ----------------------------
    if user_id:
        user_db = get_user_vectorstore(user_id)
        if user_db:  # user may not have uploaded anything
            user_docs = user_db.similarity_search(user_query, k=k_user)
            if user_docs:
                user_text = "\n\n".join([doc.page_content for doc in user_docs])
                combined_context += f"User Docs ({user_id}):\n" + user_text + "\n\n"
                sources.extend([doc.metadata.get("source", f"user_{user_id}") for doc in user_docs])

    return combined_context, sources
