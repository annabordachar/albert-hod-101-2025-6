from src.ingestion.load_book import load_book_html
from src.ingestion.chunking import chunk_paragraphs

paras = load_book_html("data/pg2267-images.html")
chunks = chunk_paragraphs(paras)

print(len(chunks))
print(len(chunks[0]["text"]))
print(chunks[0]["paragraph_ids"])
