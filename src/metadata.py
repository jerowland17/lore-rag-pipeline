import yaml


def parse_metadata(text: str) -> dict:
    """
    Split YAML frontmatter from the markdown body.
    Return {"metadata": {...}, "body": "..."}.
    """
    parts = text.split("---", 2)   # split text, keep the list

    if len(parts) < 3:
        
        return {"metadata": {}, "body": text.strip()}
    
    yaml_part = parts[1]          # the YAML piece
    body_part = parts[2]          # the body piece

    yaml_part_safe_load = yaml.safe_load(yaml_part)

    body_part_striped = body_part.strip()

    return {"metadata": yaml_part_safe_load, "body": body_part_striped}



if __name__ == "__main__":
    # A fake file's contents to test against — no disk reading needed yet.
    sample = """---
title: Test Title
category: geography
tags: [a, b, c]
---

# A Heading

Some body prose here.
"""
    # Call your function on the sample and print the result
    # so you can eyeball whether metadata and body look right.
    result = parse_metadata(sample)
    print("METADATA:", result["metadata"])
    print("BODY:", result["body"])

    sample2 = """# Just a Heading

Some prose with no frontmatter at all.
"""
    result2 = parse_metadata(sample2)
    print("METADATA2:", result2["metadata"])
    print("BODY2:", result2["body"])
