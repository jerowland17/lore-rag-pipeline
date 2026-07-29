from pathlib import Path

def load_lore_files(raw_dir: str) -> list[dict]:
    """
    Find every .md file in raw_dir, read its text, and return a list of
    dicts like: {"source": "geography_the_shattered_reach.md", "text": "..."}
    """
    results = []                                  
    for path in Path(raw_dir).glob("*.md"):       
        item = {"source": path.name, "text": path.read_text(encoding="utf-8")}
        results.append(item) # append it to results
    return results       

if __name__ == "__main__":
    lore = load_lore_files("data/raw")
    print(f"Loaded {len(lore)} files")
    for item in lore:
        print(item["source"], "-", len(item["text"]), "characters")                        