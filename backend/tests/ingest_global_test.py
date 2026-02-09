from backend.rag.ingest_global import ingest_global_pdf

# Ingest all global PDFs
ingest_global_pdf("backend/rag/docs/Sample.pdf")
ingest_global_pdf("backend/rag/docs/Brand Book - Pi Dot.pdf")
ingest_global_pdf("backend/rag/docs/IV DELTA DATABASE  modified.pdf")
ingest_global_pdf("backend/rag/docs/Dinesh_Resume (2).pdf")

print("All global PDFs ingested successfully ✅")
