from backend.rag.ingest_global import get_global_vectorstore

db = get_global_vectorstore()
docs = db.similarity_search("text from your PDF here", k=3)
for d in docs:
    print(d.page_content)







# from backend.rag.retriever import retrieve_context

# query = "What is this document about?"

# context = retrieve_context(query)

# print("\n===== CONTEXT =====\n")
# print(context)





# from backend.rag.retriever import retrieve_context

# print(retrieve_context("your question"))





# from rag.ingest import ingest_pdf

# # Run ingestion
# count = ingest_pdf("backend/rag/Sample.pdf")

# print("✅ Chunks stored:", count)





# from rag.retrieve import retrieve_context

# query = "Summarize this document"

# context = retrieve_context(query)

# print("\n🔎 Retrieved Context:\n")
# print(context)

