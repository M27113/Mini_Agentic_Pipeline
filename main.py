import sys
import os
import time
import argparse
from dotenv import load_dotenv
from modules.controller import Pipeline
from openai import AuthenticationError, RateLimitError, APIConnectionError
    
def load_queries(file_path):
        # added try except for better error handling
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"[Error] Queries file not found: {file_path}")
        return []
    except Exception as e:
        print(f"[Error] Failed to load queries from {file_path} → {e}")
        return []

def main():
        # added try except for better error handling
    try:
        load_dotenv()  # load .env
        if not os.getenv("OPENAI_API_KEY"):
            print("[Warning] OPENAI_API_KEY not set in .env file")
        if not os.getenv("TAVILY_API_KEY"):
            print("[Warning] TAVILY_API_KEY not set in .env file")

        parser = argparse.ArgumentParser(description="Mini Agentic Pipeline")
        parser.add_argument("--docs-path", default="kb_docs", help="Path to KB documents")
        parser.add_argument("--queries-file", default="queries.txt", help="File containing queries")
        parser.add_argument(
            "--prompt-version", 
            type=str, 
            default="v2", 
            choices=["v1", "v2"], 
            help="Prompt version to use"
        )
        args = parser.parse_args()

        queries = load_queries(args.queries_file)
        if not queries:
            print("[Info] No queries found in the file. Exiting.")
            sys.exit(0) # exit gracefully if no queries

        pipeline = Pipeline(docs_path=args.docs_path, prompt_version=args.prompt_version)

        # Retry logic for RateLimitError
        MAX_RETRIES = 3
        RETRY_DELAY = 5  # seconds
        retries = 0
        while retries < MAX_RETRIES:
            try:
                all_answers, all_traces = pipeline.run_queries(
                    queries,
                    save_path_txt="answers.txt",
                    save_path_json="answers_trace.json"
                )
                break  # success
            except RateLimitError:
                retries += 1
                print(f"Rate limit hit. Retrying ({retries}/{MAX_RETRIES}) after {RETRY_DELAY}s...")
                time.sleep(RETRY_DELAY)
        else:
            print("[Error] Rate limit exceeded: You are sending too many requests to OpenAI API. Try again later.")
            sys.exit(1)

        print(f"\nPipeline executed successfully! ✅")
        print(f"Processed {len(queries)} queries.")
        print("Outputs saved as:")
        print(" - answers.txt (truncated answers for readability)")
        print(" - answers_trace.json (full answers and reasoning trace)")
            
    except AuthenticationError:
        print("[Error] Authentication failed: Please check your OpenAI API key in the .env file.")
        sys.exit(1)
    except APIConnectionError:
        print("[Error] API connection error: Please check your internet connection and try again.")
        sys.exit(1)
    except Exception as e:
        print(f"[Error] An unexpected error occurred while running the pipeline: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

