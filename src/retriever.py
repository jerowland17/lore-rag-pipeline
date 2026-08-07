import chromadb
from sentence_transformers import SentenceTransformer

def retrieve(question: str, n_results: int = 3, where: dict | None = None,
             persist_dir: str = "data/processed/chroma",
             collection_name: str = "lore",
             model_name: str = "all-MiniLM-L6-v2") -> list[dict]:
    """
    Embed `question`, search the lore collection, and return the top
    `n_results` chunks as:
    [{"text": ..., "metadata": {...}, "distance": 0.42}, ...]
    """
    # 1. load model, encode the question
    # 2. open client + collection
    # 3. results = collection.query(...)
    # 4. loop and build the output list

    model = SentenceTransformer(model_name)
    vector = model.encode(question)
    client = chromadb.PersistentClient(path=persist_dir)
    collection = client.get_collection(name=collection_name)
    results = collection.query(
        query_embeddings=[vector.tolist()],
        n_results=n_results,
        where=where,
        include=["documents", "metadatas", "distances"],
    )

    docs = results["documents"] or [[]]
    metas = results["metadatas"] or [[]]
    dists = results["distances"] or [[]]

    output = []
    for text, meta, dist in zip(docs[0], metas[0], dists[0]):
        output.append({"text": text, "metadata": meta, "distance": dist})
    return output


if __name__ == "__main__":
    hits = retrieve("Who rules the mountain clans?")
    for hit in hits:
        print(round(hit["distance"], 3), hit["metadata"]["source"])
        print(hit["text"][:200])
        print("---")