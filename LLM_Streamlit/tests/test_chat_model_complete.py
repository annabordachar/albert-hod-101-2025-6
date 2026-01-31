from src.llm.chat_model import complete

res = complete(
    messages=[{"role": "user", "content": "Say hello in one sentence."}]
)

print(res)
