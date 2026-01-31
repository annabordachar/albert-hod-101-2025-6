from src.ingestion.load_book import load_book_html

paras = load_book_html("data/pg2267-images.html")

print(f"Paragraphs: {len(paras)}")
print(paras[0])
print(paras[50])
print(paras[-1])


# To launch test LLM_Streamlit % python -m tests.test_load_book