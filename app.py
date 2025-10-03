from flask import Flask, request, jsonify
from flask_cors import CORS
from modules.controller import Pipeline
import copy
import sys
import json

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests if needed

# Initialize pipeline once
docs_path = "C:\\Users\\Balanagaiah\\Desktop\\Mini_Agentic_Pipeline\\kb_docs"  # Adjust as needed
try:
    pipeline = Pipeline(docs_path=docs_path, prompt_version="v2")
except FileNotFoundError as fnf_error:
    print(f"[Error] KB folder not found: {fnf_error}")
    sys.exit(1)
except Exception as e:
    print(f"[Error] Failed to initialize pipeline: {e}")
    sys.exit(1)


@app.route("/query", methods=["POST"])
def query_pipeline():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No JSON payload received"}), 400

        queries = data.get("queries")
        truncate = data.get("truncate", True)  # optional flag for truncated answers

        # Validation
        if not queries or not isinstance(queries, list) or not all(isinstance(q, str) for q in queries):
            return jsonify({"error": "Queries must be a list of strings"}), 400

        # Optional: limit number of queries to prevent overload
        queries = queries[:10]

        # Run pipeline
        answers, traces = pipeline.run_queries(queries)

        # Save truncated answers to text file
        try:
            with open("answers.txt", "w", encoding="utf-8") as f:
                for ans in answers:
                    f.write(ans + "\n\n")
            print("[Info] Answers saved to answers.txt")
        except Exception as e:
            print(f"[Warning] Could not save answers.txt: {e}")

        # Save full traces to JSON file
        try:
            serializable_traces = copy.deepcopy(traces)
            for trace in serializable_traces.values():
                trace["reasoning_trace"] = {k: str(v) for k, v in trace["reasoning_trace"].items()}
            with open("answers_trace.json", "w", encoding="utf-8") as f:
                json.dump(serializable_traces, f, indent=4, ensure_ascii=False)
            print("[Info] Traces saved to answers_trace.json")
        except Exception as e:
            print(f"[Warning] Could not save answers_trace.json: {e}")

        # Handle optional truncation for API response
        if truncate:
            truncated_answers = [ans[:500] + "..." if len(ans) > 500 else ans for ans in answers]
        else:
            truncated_answers = answers

        return jsonify({
            "answers": truncated_answers,
            "traces": serializable_traces
        })

    except Exception as e:
        print(f"[Exception] {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
