from dotenv import load_dotenv

load_dotenv()

from sentence_transformers  import SentenceTransformer

def embed_chunks(chunks: list[dict], model_name: str = "all-MiniLM-L6-v2") -> list[dict]:
    model = SentenceTransformer(model_name)
    values = [chunk["text"] for chunk in chunks]
    vectors = model.encode(values)

    results = []
    for chunk, vector in zip(chunks, vectors):
        chunk_vector = {"source": chunk["source"], "metadata": chunk["metadata"], 
                      "text": chunk["text"], "embedding": vector}
        results.append(chunk_vector)
        
    return results

if __name__ == "__main__":
    from src.pipeline import load_and_parse
    from src.chunky import chunk_documents 

    items = load_and_parse("data/raw")
    chunks = chunk_documents(items)
    embedded = embed_chunks(chunks)

    print(f"Embedded {len(embedded)} chunks")
    print(len(embedded[0]["embedding"]))
