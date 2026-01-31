from src.rag.retriever import retrieve_chunks

chunks = retrieve_chunks(
    "Why does Iago hate Othello?",
    k=5,
)

for c in chunks:
    print(c["chunk_id"])
    print(c["paragraph_ids"])
    print(c["text"][:200])
    print("----")
