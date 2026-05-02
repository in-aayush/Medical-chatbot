from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from transformers import pipeline
from sentence_transformers import CrossEncoder

# 🔹 Global memory
chat_history = []

# 🔹 Reranker
reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")


def load_db():
    embedding = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    db = FAISS.load_local(
        "faiss_index",
        embedding,
        allow_dangerous_deserialization=True
    )
    return db


def load_llm():
    generator = pipeline(
        "text-generation",   # ✅ fixed
        model="google/flan-t5-base",
        max_length=512
    )
    return generator


# 🔥 Query expansion
def expand_query(query):
    q = query.lower()

    if "pcl" in q:
        return query + " posterior cruciate ligament knee joint ligament"

    if "acl" in q:
        return query + " anterior cruciate ligament knee"

    return query + " medical explanation"


# 🔥 Rerank function
def rerank_docs(query, docs):
    pairs = [(query, doc.page_content) for doc in docs]
    scores = reranker.predict(pairs)

    ranked = sorted(zip(scores, docs), key=lambda x: x[0], reverse=True)
    return [doc for _, doc in ranked[:3]]

def is_medical_query(query):
    medical_keywords = [
        "pain", "disease", "treatment", "symptom",
        "fever", "infection", "injury", "diabetes",
        "cancer", "blood", "fracture", "ligament"
    ]
    
    query = query.lower()
    return any(word in query for word in medical_keywords)

def get_answer(query):
    global chat_history

    db = load_db()
    llm = load_llm()

    query_expanded = expand_query(query)

    # 🔍 Retrieve more docs
    docs = db.similarity_search(query_expanded, k=8)

    # 🔥 Keyword filtering
    filtered_docs = []
    for doc in docs:
        text = doc.page_content.lower()

        if any(word in text for word in query.lower().split()):
            filtered_docs.append(doc)

    docs = filtered_docs if filtered_docs else docs

    # 🔥 Rerank
    docs = rerank_docs(query, docs)

    # ❌ Fallback
    if not docs:
        response = llm(f"Explain clearly: {query}")
        return response[0]["generated_text"]

    # 🧠 Context
    context = " ".join([doc.page_content for doc in docs])
    context = context.replace("\n", " ").replace("  ", " ")

    # 🧠 Memory
    history_text = ""
    for q, a in chat_history[-3:]:
        history_text += f"User: {q}\nBot: {a}\n"

    prompt = f"""
    Answer the question in a clear and simple way.

    Context:
    {context}

    Question: {query}

    Answer:
    """

    response = llm(prompt)
    answer = response[0]["generated_text"]

    chat_history.append((query, answer))

    return answer