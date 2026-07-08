import chromadb
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

def dataframe_to_documents(df):
    documents = []

    for index, row in df.iterrows():
        text = " | ".join([f"{col}: {row[col]}" for col in df.columns])
        documents.append({
            "id": str(index),
            "text": text
        })

    return documents


def create_rag_collection(df):
    client = chromadb.Client()

    try:
        client.delete_collection("business_rag")
    except:
        pass

    collection = client.create_collection(name="business_rag")

    documents = dataframe_to_documents(df)

    texts = [doc["text"] for doc in documents]
    ids = [doc["id"] for doc in documents]

    embeddings = model.encode(texts).tolist()

    collection.add(
        ids=ids,
        documents=texts,
        embeddings=embeddings
    )

    return collection


def retrieve_context(collection, question, top_k=5):
    question_embedding = model.encode([question]).tolist()

    results = collection.query(
        query_embeddings=question_embedding,
        n_results=top_k
    )

    retrieved_docs = results["documents"][0]

    return "\n".join(retrieved_docs)