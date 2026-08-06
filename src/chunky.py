from langchain_text_splitters import RecursiveCharacterTextSplitter


def chunk_documents(items: list[dict], chunk_size: int = 500, chunk_overlap: int = 50) -> list[dict]:
    """
    Split each item's "body" into smaller text chunks, carrying source +
    metadata onto every chunk. Return a list of dicts like:
    {"source": ..., "metadata": {...}, "text": "<chunk text>"}
    """

    chunky_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)

    results = []
    for item in items:
        chunk = chunky_splitter.split_text(item["body"])

        for sub_chunks in chunk:
            chunk_dict = {"source": item["source"], "metadata": item["metadata"], "text": sub_chunks}
            results.append(chunk_dict)

    return results
            
if __name__ == "__main__":
    from src.pipeline import load_and_parse

    items = load_and_parse("data/raw")
    chunks = chunk_documents(items)

    print(f"Loaded {len(items)} files, split into {len(chunks)} chunks")

    for chunk in chunks[:3]:
        print(chunk["source"], "-", len(chunk["text"]), "characters")
        print(chunk["text"])
        print("---")