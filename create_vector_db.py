from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

# 1. Load our knowledge-base documents
loader = DirectoryLoader(
    "knowledge_base",
    glob="*.txt",
    loader_cls=TextLoader
)

documents = loader.load()

print("Documents loaded:", len(documents))

# 2. Split documents into smaller chunks
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

chunks = splitter.split_documents(documents)

print("Chunks created:", len(chunks))

# 3. Create embeddings using our local Ollama model
embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)

# 4. Store the chunks + embeddings in Chroma
vector_db = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="./chroma_db"
)

print("Vector database created successfully!")