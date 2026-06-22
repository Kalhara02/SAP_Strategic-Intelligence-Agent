import ollama

response = ollama.chat(
    model="qwen3:8b",
    messages=[
        {
            "role": "user",
            "content": "What is SAP?"
        }
    ]
)

print(response["message"]["content"])