import argparse

from src.generate import generate


def main():
    parser = argparse.ArgumentParser(
        description="Ask a question about the Shattered Reach lore and get a cited answer."
    )
    parser.add_argument(
        "question",
        help="The question to ask. Wrap it in quotes.",
    )
    parser.add_argument(
        "-n",
        "--n-results",
        type=int,
        default=3,
        help="How many lore chunks to retrieve (default: 3).",
    )
    parser.add_argument(
        "--category",
        help="Only search chunks in this category, e.g. geography.",
    )
    args = parser.parse_args()

    where = {"category": args.category} if args.category else None

    result = generate(args.question, n_results=args.n_results, where=where)

    print(result["answer"])

    if result["hits"]:
        print("\n--- sources ---")
        for i, hit in enumerate(result["hits"], start=1):
            print(f"[{i}] {hit['metadata']['source']} (distance {hit['distance']:.3f})")


if __name__ == "__main__":
    main()