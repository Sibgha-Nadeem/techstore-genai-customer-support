# TechStore AI Customer Support Assistant

An AI-powered customer support chatbot built using **RAG (Retrieval-Augmented Generation)**. The assistant retrieves relevant information from a knowledge base and uses a locally running LLM to generate natural-language responses.

The project includes a **React frontend**, **FastAPI backend**, semantic search using embeddings, and **Llama 3.2 running locally through Ollama**.

## Features

- AI-powered customer support chatbot
- Retrieval-Augmented Generation (RAG)
- Semantic search over a customer-support knowledge base
- Product information lookup
- Shipping and delivery information
- Return policy questions
- Warranty questions
- Payment method questions
- Follow-up conversation handling
- Multi-part question handling
- Relevance checking to avoid answering unsupported questions
- Local LLM inference using Ollama
- React-based chat interface
- FastAPI REST API

## How It Works

The system follows this flow:

```text
Customer
   ↓
React Chat Interface
   ↓
FastAPI Backend
   ↓
Question Processing
   ↓
Semantic Search
   ↓
Relevant Knowledge
   ↓
Llama 3.2
   ↓
AI-generated Response
   ↓
React Chat Interface
```

### RAG Pipeline

The knowledge base contains fictional TechStore information such as products, shipping, returns, payments, and warranties.

The documents are processed into smaller chunks and converted into numerical embeddings using `nomic-embed-text`.

When a customer asks a question:

1. The question is converted into an embedding.
2. The system compares it with the stored knowledge embeddings.
3. The most relevant information is retrieved.
4. The retrieved information is provided to Llama 3.2.
5. Llama 3.2 generates the final response.

This helps the assistant answer using the available knowledge rather than relying entirely on the model's general knowledge.

## Technology Stack

### Frontend

- React.js
- Vite
- JavaScript
- CSS

### Backend

- Python
- FastAPI
- Uvicorn

### AI / RAG

- Llama 3.2
- Ollama
- LangChain
- Ollama Embeddings
- `nomic-embed-text`
- Cosine similarity

## Project Structure

```text
techstore-genai-customer-support/
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── ...
│   ├── package.json
│   └── package-lock.json
│
├── knowledge_base/
│   ├── products.txt
│   ├── payment_methods.txt
│   ├── return_policy.txt
│   ├── shipping_policy.txt
│   └── warranty_policy.txt
│
├── build_knowledge.py
├── main.py
├── rag.py
├── read_knowledge.py
├── test_embeddings.py
├── .gitignore
└── README.md
```

## Requirements

Before running the project, install:

- Python 3.13+
- Node.js
- npm
- Ollama

You also need the following Ollama models:

```bash
ollama pull llama3.2
ollama pull nomic-embed-text
```

## Backend Setup

Create and activate a Python virtual environment:

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

Install the required Python packages:

```bash
pip install fastapi uvicorn langchain langchain-community langchain-ollama ollama
```

Build the knowledge embeddings:

```bash
python build_knowledge.py
```

Start the FastAPI server:

```bash
uvicorn main:app --reload
```

The backend will run at:

```text
http://127.0.0.1:8000
```

FastAPI documentation is available at:

```text
http://127.0.0.1:8000/docs
```

## Frontend Setup

Open another terminal and move into the frontend directory:

```bash
cd frontend
```

Install the frontend dependencies:

```bash
npm install
```

Start the React development server:

```bash
npm run dev
```

The frontend will normally be available at:

```text
http://localhost:5173
```

## Example Questions

The assistant can answer questions such as:

```text
How long does standard shipping take?

How long does express shipping take?

Can I return an item after 10 days?

How long does a refund take?

Do you accept Mastercard?

How much is the TechPhone X?

Does the warranty cover accidental damage?
```

It can also handle follow-up questions such as:

```text
Customer: How long does shipping take?

Assistant: Standard shipping usually takes 3–5 business days.

Customer: What about express?

Assistant: Express shipping usually takes 1–2 business days.
```

The assistant can also handle multi-part questions:

```text
Can I return a laptop after 10 days, and how long will the refund take?
```

## Knowledge Limitations

The assistant is intentionally designed to avoid making up information.

If a question is not covered by the knowledge base, the system can respond that the available information does not specify the answer.

For example:

```text
Customer: Do you offer student discounts?

Assistant: I don't have enough information in the knowledge base to answer that.
```

This helps reduce hallucinations and keeps responses grounded in the available information.

## Conversation Ending

The chatbot also recognizes common conversation-ending messages such as:

```text
bye
goodbye
exit
quit
```

and responds with a closing message instead of sending the request through the RAG pipeline.

## Privacy and Data

This project uses a fictional company called **TechStore** and self-created sample customer-support information.

No private company data, customer information, credentials, or confidential business information is used in the knowledge base.

The language model runs locally through Ollama, so the project does not require sending customer-support questions to a paid external LLM API.

## Future Improvements

Possible future improvements include:

- Persistent conversation history
- New Chat button
- Typing indicator
- Improved error handling
- Source citations in responses
- Better semantic search
- Persistent vector database
- User authentication
- Conversation logging with privacy controls
- Deployment of the FastAPI backend
- Deployment of the React frontend

## Project Purpose

This project was created to explore practical applications of **Generative AI, RAG, semantic search, LLMs, and full-stack AI applications**.

It demonstrates how an AI assistant can combine a knowledge base with a locally running language model to provide grounded customer-support responses.
