from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
import json


# --------------------------------------------------
# 1. LOAD KNOWLEDGE BASE
# --------------------------------------------------

loader = DirectoryLoader(
    "knowledge_base",
    glob="*.txt",
    loader_cls=TextLoader
)

documents = loader.load()

print("Documents loaded:", len(documents))


# --------------------------------------------------
# 2. SPLIT DOCUMENTS INTO CHUNKS
# --------------------------------------------------

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

chunks = splitter.split_documents(documents)

print("Chunks created:", len(chunks))


# --------------------------------------------------
# 3. CREATE EMBEDDING MODEL
# --------------------------------------------------

embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)


# --------------------------------------------------
# 4. CREATE EMBEDDINGS
# --------------------------------------------------

knowledge_data = []

for chunk in chunks:

    vector = embeddings.embed_query(
        chunk.page_content
    )

    source = chunk.metadata.get(
        "source",
        "unknown"
    )

    knowledge_data.append({
        "text": chunk.page_content,
        "vector": vector,
        "source": source
    })


# --------------------------------------------------
# 5. SAVE EVERYTHING
# --------------------------------------------------

with open(
    "knowledge_embeddings.json",
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        knowledge_data,
        file
    )


print("Knowledge embeddings saved successfully.")
print("Saved chunks:", len(knowledge_data))