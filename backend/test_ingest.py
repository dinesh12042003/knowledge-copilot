# from rag.ingest import ingest_pdf

# # Run ingestion
# count = ingest_pdf("backend/rag/Sample.pdf")

# print("✅ Chunks stored:", count)

from rag.retrieve import retrieve_context

query = "Summarize this document"

context = retrieve_context(query)

print("\n🔎 Retrieved Context:\n")
print(context)

