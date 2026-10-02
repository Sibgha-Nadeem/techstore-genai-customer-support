import json
import math
import ollama

from langchain_ollama import OllamaEmbeddings


# --------------------------------------------------
# 1. LOAD SAVED KNOWLEDGE
# --------------------------------------------------

with open(
    "knowledge_embeddings.json",
    "r",
    encoding="utf-8"
) as file:

    chunk_vectors = json.load(file)

print("Knowledge loaded:", len(chunk_vectors), "chunks")


# --------------------------------------------------
# 2. CREATE EMBEDDING MODEL
# --------------------------------------------------

embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)
# --------------------------------------------------
# 3. CONVERSATION HISTORY
# --------------------------------------------------

conversation_history = []

# --------------------------------------------------
# 3. COSINE SIMILARITY
# --------------------------------------------------

def cosine_similarity(vector1, vector2):

    dot_product = 0
    length1 = 0
    length2 = 0

    for i in range(len(vector1)):

        dot_product += vector1[i] * vector2[i]

        length1 += vector1[i] * vector1[i]

        length2 += vector2[i] * vector2[i]

    length1 = math.sqrt(length1)
    length2 = math.sqrt(length2)

    if length1 == 0 or length2 == 0:
        return 0

    return dot_product / (length1 * length2)

# --------------------------------------------------
# REWRITE FOLLOW-UP QUESTION
# --------------------------------------------------

def rewrite_question(question):

    if len(conversation_history) == 0:

        return question

    history_text = ""

    for conversation in conversation_history:

        history_text += (
            "Customer: "
            + conversation["customer"]
            + "\n"
        )

        history_text += (
            "Assistant: "
            + conversation["assistant"]
            + "\n"
        )

    prompt = f"""
You are helping a customer support system understand follow-up questions.

Look at the previous conversation and the customer's new question.

Rewrite the new question as a complete standalone question.

Keep the original meaning.
Keep ALL parts of the original question.

Do not remove any options, alternatives, comparisons, or parts of the question.

If the customer asks about two things, keep both things in the rewritten question.

If the new question is already clear by itself, return it unchanged.

Do not answer the question.

Only return the rewritten question.

Previous conversation:
{history_text}

New customer question:
{question}

Standalone question:
"""

    response = ollama.chat(
        model="llama3.2",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        options={
            "temperature": 0
        }
    )

    rewritten_question = response["message"]["content"].strip()

    return rewritten_question
# --------------------------------------------------
# 4. SEARCH KNOWLEDGE
# --------------------------------------------------

def search_knowledge(question):

    question_vector = embeddings.embed_query(question)

    results = []

    for item in chunk_vectors:

        score = cosine_similarity(
            question_vector,
            item["vector"]
        )

        results.append({
            "text": item["text"],
            "score": score,
            "source": item["source"]
        })

    # Highest similarity first
    results.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    return results

import ollama


# --------------------------------------------------
# 5. GENERATE ANSWER
# --------------------------------------------------

# --------------------------------------------------
# 5. GENERATE ANSWER
# --------------------------------------------------

def generate_answer(question, relevant_information):

    prompt = f"""
You are a customer support assistant for TechStore.

Answer the customer's question using ONLY the knowledge provided below.

IMPORTANT RULES:

1. Read the knowledge carefully before answering.

2. Answer exactly what the customer asked.

3. Pay close attention to numbers, dates, and time periods.

4. When comparing numbers, perform the comparison correctly.

5. If a policy says something is allowed "within" a certain number
   of days, the smaller number of days is still inside that limit.

6. For example:
   - The return policy says returns are accepted within 30 days.
   - 10 days is less than 30 days.
   - Therefore, an item purchased 10 days ago is still within
     the 30-day return period.

7. Do NOT say that 10 days is outside a 30-day return period.

8. Do not reverse the meaning of a policy.

9. Use ONLY facts that are explicitly stated in the Knowledge section.

10. Never assume or invent a policy, product, payment method,
    discount, warranty, or service.

11. If the knowledge does not contain the answer, say:
    "I don't have enough information in the knowledge base to answer that."

12. If the question contains multiple parts, answer each part using
    only the facts explicitly stated in the Knowledge section.

Knowledge:
{relevant_information}

Customer question:
{question}

Give a short, clear answer:
"""

    response = ollama.chat(
        model="llama3.2",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        options={
            "temperature": 0
        }
    )

    answer = response["message"]["content"]

    return answer