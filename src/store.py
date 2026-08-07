import chromadb

def store_chunks(embedded: list[dict], persist_dir: str = "data/processed/chroma",
                 collection_name: str = "lore") -> None:
    
    client = chromadb.PersistentClient(path=persist_dir)
    collection = client.get_or_create_collection(name=collection_name)

    ids = []
    documents = []
    embeddings = []
    metadatas = []

    counts = {}

    for chunk in embedded:
        source = chunk["source"]
        index = counts.get(source, 0)
        counts[source] = index + 1

        ids.append(f"{source}-{index}")
        documents.append(chunk["text"])
        embeddings.append(chunk["embedding"].tolist())

        meta = chunk["metadata"]
        metadatas.append({
        "source": chunk["source"],
        "title": meta.get("title", ""),
        "category": meta.get("category", ""),
        "era": meta.get("era", ""),
        "tags": ", ".join(meta.get("tags", []))})
    collection.upsert(ids=ids, documents=documents, embeddings=embeddings, metadatas=metadatas)


if __name__ == "__main__":
    from src.pipeline import load_and_parse
    from src.chunky import chunk_documents 
    from src.embedder import embed_chunks

    items = load_and_parse("data/raw")
    chunks = chunk_documents(items)
    embedded = embed_chunks(chunks)
    store_chunks(embedded)
    client = chromadb.PersistentClient(path="data/processed/chroma")
    collection = client.get_collection(name="lore")
    

    print(f"Embedded {len(embedded)} chunks")
    print(len(embedded[0]["embedding"]))
    print(collection.count())
    print(collection.get(ids=["geography_the_shattered_reach.md-0"], include=["metadatas", "documents"]))

