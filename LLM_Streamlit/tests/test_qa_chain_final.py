from src.rag.qa_chain import answer_question

res = answer_question("Why does Iago hate Othello?")

print(res["answer"])
print("\nSources:")
for c in res["citations"]:
    print("-", c)
