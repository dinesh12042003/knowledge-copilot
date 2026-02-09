from backend.rag.vectorstore.vectorstore import get_vectorstore
from backend.rag.ingest_user import get_user_vectorstore

# ----------------------------
# Simple Retrieval for Testing
# ----------------------------
def get_context(query: str, user_id: str = None, k_global=3, k_user=3):
    """
    Returns combined context from global and user docs for a query.
    This is a simpler version for testing.
    """

    combined_context = ""

    # ----------------------------
    # 1️⃣ Global documents
    # ----------------------------
    global_db = get_vectorstore()
    global_docs = global_db.similarity_search(query, k=k_global)
    global_text = "\n\n".join([doc.page_content for doc in global_docs])
    if global_text:
        combined_context += "Global Docs:\n" + global_text + "\n\n"

    # ----------------------------
    # 2️⃣ User-specific documents
    # ----------------------------
    if user_id:
        user_db = get_user_vectorstore(user_id)
        if user_db:
            user_docs = user_db.similarity_search(query, k=k_user)
            user_text = "\n\n".join([doc.page_content for doc in user_docs])
            if user_text:
                combined_context += f"User Docs ({user_id}):\n" + user_text + "\n\n"

    return combined_context
