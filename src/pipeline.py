from src.loader import load_lore_files
from src.metadata import parse_metadata
from src.chunky import chunk_documents

def load_and_parse(raw_dir: str) -> list[dict]:
    """
    Load every lore file from raw_dir, then split each one's text into
    metadata + body. Return a list of dicts like:
    {"source": "geography_the_shattered_reach.md", "metadata": {...}, "body": "..."}
    """

    results = []
    for path in load_lore_files(raw_dir):
        item = parse_metadata(path["text"])
        item["source"] = path["source"]
        results.append(item)
    return results


def load_parse_and_chunk(raw_dir: str) -> list[dict]:
    chunks = chunk_documents(load_and_parse(raw_dir))
    return chunks


if __name__ == "__main__":
    chunks = load_parse_and_chunk("data/raw")
    print(f"Loaded and parsed {len(chunks)} chunks")
    for chunk in chunks[:3]:
        print(chunk["source"], "-", len(chunk["text"]), "characters")
        print(chunk["text"])
        print("---")
