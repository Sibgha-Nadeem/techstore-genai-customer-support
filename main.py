from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from rag import (
    search_knowledge,
    generate_answer,
    rewrite_question,
    conversation_history
)


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# This describes the data we expect from the customer
class Question(BaseModel):

    question: str


@app.get("/")
def home():

    return {
        "message": "TechStore Customer Support API is running"
    }


@app.post("/ask")
def ask_question(data: Question):

    question = data.question

    # Rewrite the question if it is a follow-up
    search_question = rewrite_question(question)

    # Search using the rewritten question
    results = search_knowledge(search_question)

    # Check if the question is relevant
    RELEVANCE_THRESHOLD = 0.60

    if results[0]["score"] < RELEVANCE_THRESHOLD:

        answer = (
            "I don't have enough information in the knowledge base "
            "to answer that."
        )

        conversation_history.append(
            {
                "customer": question,
                "assistant": answer
            }
        )

        return {
            "question": question,
            "answer": answer
        }

    # Find the most relevant source
    best_source = results[0]["source"]

    # Keep chunks from the most relevant source
    source_results = []

    for result in results:

        if result["source"] == best_source:

            source_results.append(result)

    # Build the information given to Llama
    relevant_information = ""

    for result in source_results:

        relevant_information += (
            "\n"
            + result["text"]
            + "\n"
        )

    # Generate the final answer
    answer = generate_answer(
        question,
        relevant_information
    )

    # Save conversation
    conversation_history.append(
        {
            "customer": question,
            "assistant": answer
        }
    )

    return {
        "question": question,
        "answer": answer
    }