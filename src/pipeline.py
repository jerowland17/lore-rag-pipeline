from src.loader import load_lore_files
from src.metadata import parse_metadata


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

if __name__ == "__main__":
    items = load_and_parse("data/raw")
    print(f"Loaded and parsed {len(items)} files")
    for item in items:
        print(item["source"], "-", item["metadata"])
