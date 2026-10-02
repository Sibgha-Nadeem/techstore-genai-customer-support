import ollama

response = ollama.chat(
    model="llama3.2",
    messages=[
        {
            "role": "user",
            "content": "Say hello and explain in one sentence what a customer support assistant does."
        }
    ]
)

print(response["message"]["content"])