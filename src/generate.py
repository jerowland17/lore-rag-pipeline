from dotenv import load_dotenv

load_dotenv()

import anthropic

from src.retriever import retrieve

MODEL = "claude-opus-5"

SYSTEM_PROMPT = """You are a lore librarian for a fictional world.

Answer the user's question using ONLY the lore excerpts provided in their message.
Rules:
- If the excerpts do not contain the answer, say so plainly. Do not invent lore.
- Cite the excerpts you used by their number, like [1] or [2][3].
- Keep answers concise: a short paragraph unless the question needs more.
"""


def format_context(hits: list[dict]) -> str:
    """
    Turn retrieved chunks into a numbered block of text the model can cite.

    [1] source=geography_the_shattered_reach.md | title=... | era=...
    <chunk text>
    """
    blocks = []
    for i, hit in enumerate(hits, start=1):
        meta = hit["metadata"]
        header = (
            f"[{i}] source={meta.get('source', '')} "
            f"| title={meta.get('title', '')} "
            f"| category={meta.get('category', '')} "
            f"| era={meta.get('era', '')}"
        )
        blocks.append(f"{header}\n{hit['text']}")
    return "\n\n".join(blocks)


def build_prompt(question: str, hits: list[dict]) -> str:
    """Assemble the single user message: excerpts first, question last."""
    return (
        "Here are the most relevant lore excerpts:\n\n"
        f"{format_context(hits)}\n\n"
        f"Question: {question}"
    )


def generate(question: str, n_results: int = 3, where: dict | None = None,
             model: str = MODEL) -> dict:
    """
    Retrieve the top `n_results` lore chunks for `question`, then ask Claude to
    answer using only those chunks.

    Returns {"answer": str, "hits": list[dict]} so the caller can show sources.
    """
    hits = retrieve(question, n_results=n_results, where=where)

    if not hits:
        return {"answer": "No lore found for that question.", "hits": []}

    client = anthropic.Anthropic()
    response = client.messages.create(
        model=model,
        max_tokens=4000,
        system=SYSTEM_PROMPT,
        output_config={"effort": "low"},
        messages=[{"role": "user", "content": build_prompt(question, hits)}],
    )

    answer = "".join(
        block.text for block in response.content if block.type == "text"
    )
    return {"answer": answer, "hits": hits}


if __name__ == "__main__":
    result = generate("Who rules the mountain clans?")

    print(result["answer"])
    print("\n--- sources ---")
    for i, hit in enumerate(result["hits"], start=1):
        print(f"[{i}] {hit['metadata']['source']} (distance {hit['distance']:.3f})")
