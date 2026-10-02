import json
import math
import ollama
from langchain_ollama import OllamaEmbeddings

conversation_history = []


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
# 4. REWRITE FOLLOW-UP QUESTION
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
# 5. SEARCH KNOWLEDGE
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


# --------------------------------------------------
# 6. CHAT WITH CUSTOMER
# --------------------------------------------------

while True:

    question = input("\nCustomer: ")

    # Allow the customer to end the conversation
    if question.lower() == "exit":

        print("\nGoodbye!")
        break


    # --------------------------------------------------
    # 7. REWRITE QUESTION FOR SEARCH
    # --------------------------------------------------

    search_question = rewrite_question(question)

    if search_question != question:

        print("\nSearch question:")
        print(search_question)


    # --------------------------------------------------
    # 8. SEARCH
    # --------------------------------------------------

    results = search_knowledge(search_question)


    # --------------------------------------------------
    # 9. CHECK RELEVANCE
    # --------------------------------------------------

    RELEVANCE_THRESHOLD = 0.60

    if results[0]["score"] < RELEVANCE_THRESHOLD:

        answer = (
            "I don't have enough information in the knowledge base "
            "to answer that."
        )

        print("\nAI Assistant:")
        print(answer)

        conversation_history.append(
            {
                "customer": question,
                "assistant": answer
            }
        )

        continue


    # --------------------------------------------------
    # 10. FIND THE MOST RELEVANT SOURCE
    # --------------------------------------------------

    best_source = results[0]["source"]

    print("\nMost relevant source:")
    print(best_source)


    # --------------------------------------------------
    # 11. KEEP CHUNKS FROM THE MOST RELEVANT SOURCE
    # --------------------------------------------------

    source_results = []

    for result in results:

        if result["source"] == best_source:

            source_results.append(result)


    # --------------------------------------------------
    # 12. SHOW RETRIEVED INFORMATION
    # --------------------------------------------------

    print("\nRetrieved information:")

    for result in source_results:

        print(
            "\nSimilarity score:",
            round(result["score"], 3)
        )

        print(
            "Source:",
            result["source"]
        )

        print(result["text"])


    # --------------------------------------------------
    # 13. BUILD CONTEXT
    # --------------------------------------------------

    relevant_information = ""

    for result in source_results:

        relevant_information += (
            "\n"
            + result["text"]
            + "\n"
        )


    # --------------------------------------------------
    # 14. CREATE RAG PROMPT
    # --------------------------------------------------

    prompt = f"""
You are a customer support assistant for TechStore.

Answer the customer's question using ONLY the knowledge provided below.

IMPORTANT RULES:
1. Read the knowledge carefully before answering.
2. Answer exactly what the customer asked.
3. Use the conversation history to understand follow-up questions.
4. Pay close attention to numbers, dates, and time periods.
5. If a policy says something is allowed "within" a certain number of days,
   compare the customer's number of days with that limit.
6. Do not reverse the meaning of a policy.
7. Do not say the customer is outside a limit when their number is smaller than the limit.
8. Use ONLY facts that are explicitly stated in the Knowledge section.
9. Never assume or infer that a product, payment method, policy, or service is available unless the Knowledge section explicitly says so.
10. If the customer asks about something that is not mentioned in the Knowledge section, say that the knowledge base does not specify it.
11. If the question contains multiple parts, answer each part using only the facts explicitly stated in the Knowledge section.

Example:
- "within 30 days" means days 1 through 30 are allowed.
- Therefore, an item after 10 days is still within 30 days.

Conversation history:
{conversation_history}

Knowledge:
{relevant_information}

Customer question:
{question}

Give a short, clear answer:
"""


    # --------------------------------------------------
    # 15. ASK LLAMA 3.2
    # --------------------------------------------------

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


    # --------------------------------------------------
    # 16. DISPLAY ANSWER
    # --------------------------------------------------

    answer = response["message"]["content"]

    print("\nAI Assistant:")
    print(answer)


    # --------------------------------------------------
    # 17. SAVE CONVERSATION
    # --------------------------------------------------

    conversation_history.append(
        {
            "customer": question,
            "assistant": answer
        }
    )