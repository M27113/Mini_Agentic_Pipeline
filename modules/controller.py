from modules.retriever import Retriever
from modules.reasoner import Reasoner
from modules.actor import Actor
import time
import json

def truncate_answer(text, max_chars=500):
    text = text.strip()
    if len(text) <= max_chars:
        return text
    return text[:max_chars].rsplit(' ', 1)[0] + "..."

class Pipeline:
    def __init__(self, docs_path, prompt_version="v1"):
        self.retriever = Retriever(docs_path)
        self.reasoner = Reasoner(prompt_version=prompt_version)
        self.actor = Actor()

    def run_queries(self, queries, save_path_txt=None, save_path_json=None):
        all_answers = []
        all_traces = {}

        for idx, query in enumerate(queries, 1):
            start_time = time.time()

            kb_results = self.retriever.get_relevant_docs(query)

            # LLM-only decision
            action, answer, reasoning_trace = self.reasoner.decide_action(query, kb_results)

            if action == "tavily_search":
                tool_start = time.time()
                answer = self.actor.web_search(query)
                tool_latency = time.time() - tool_start
                reasoning_trace["used"] = "Tavily"
            else:
                answer = kb_results.get("summary", "No relevant KB info available.")
                tool_latency = None
                reasoning_trace["used"] = "KB"

            answer = truncate_answer(answer, 500)
            latency = time.time() - start_time

            formatted_answer = (
                f"--- Query {idx}: {query} ---\n"
                f"Answer: {answer}\n"
                f"(used: {reasoning_trace['used']}, latency: {latency:.2f}s)\n\n"
            )
            print(formatted_answer)
            all_answers.append(formatted_answer)

            all_traces[query] = {
                "query": query,
                "answer": answer,
                "reasoning_trace": {
                    "prompt_version": reasoning_trace["prompt_version"],
                    "used": reasoning_trace["used"],
                    "decision_text": reasoning_trace["decision_text"]
                },
                "latency": latency,
                "tool_latency": tool_latency
            }

        if save_path_txt:
            with open(save_path_txt, "w", encoding="utf-8") as f:
                f.writelines(all_answers)

        if save_path_json:
            serializable_traces = []
            for query, trace in all_traces.items():
                serializable_traces.append({
                    "query": query,
                    "answer": trace.get("answer"),
                    "reasoning_trace": trace.get("reasoning_trace"),
                    "latency": trace.get("latency"),
                    "tool_latency": trace.get("tool_latency")
                })
            with open(save_path_json, "w", encoding="utf-8") as f:
                json.dump(serializable_traces, f, indent=4, ensure_ascii=False)

        return all_answers, all_traces
