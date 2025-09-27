import os
import argparse
from dotenv import load_dotenv
from modules.controller import Pipeline

def load_queries(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

def main():
    load_dotenv()

    parser = argparse.ArgumentParser(description="Mini Agentic Pipeline")
    parser.add_argument("--docs-path", default="kb_docs", help="Path to KB documents")
    parser.add_argument("--queries-file", default="queries.txt", help="File containing queries")
    parser.add_argument("--prompt-version", default="v2", help="Prompt version (v1, v2, ...)")
    args = parser.parse_args()

    queries = load_queries(args.queries_file)
    pipeline = Pipeline(docs_path=args.docs_path, prompt_version=args.prompt_version)

    pipeline.run_queries(
        queries,
        save_path_txt="answers.txt",
        save_path_json="answers_trace.json"
    )

if __name__ == "__main__":
    main()
