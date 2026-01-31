from src.llm.chat_model import stream_completion

msgs = [{"role": "user", "content": "Explain jealousy in one short sentence."}]

for tok in stream_completion(msgs):
    print(tok, end="", flush=True)

print()
