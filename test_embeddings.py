from langchain_ollama import OllamaEmbeddings

# Create our local embedding model
embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)

# Convert a sentence into numbers
text = "Can I pay using a credit card?"

vector = embeddings.embed_query(text)

print("Number of values in embedding:", len(vector))
print("First 10 values:", vector[:10])