#   🤖 Mini Agentic Pipeline ✨

## **Overview**

The **Mini Agentic Pipeline** is a modular AI system that:  

1. Retrieves relevant context from a **small knowledge base (KB)**.  
2. Uses an **LLM** to reason and decide the next step.  
3. Executes an **action via a tool** (Tavily web search).  
4. Produces a **final answer** along with a **step-by-step trace/log**.

The system demonstrates **agentic behavior**, dynamically deciding whether to use the KB or external tool based on the LLM’s decision.

---

## Pipeline Architecture

```bash
+-----------+     +--------------------+     +--------------------+     +-----------+     +------------+
| User Query| --> |     Retriever      | --> |     Reasoner       | --> |    KB     | --> | Final Answer|
+-----------+     |  (FAISS + KB docs) |     | (LLM decides: KB   |     +-----------+     +------------+
                  +--------------------+     |  or Tavily Tool)   |
                                             +---------+----------+
                                                       |
                                                       v
                                             +--------------------+
                                             |      Actor         |
                                             | (Tavily Web Search)|
                                             +--------------------+
                                                       |
                                                       v
                                             +--------------------+
                                             |    Trace Log       |
                                             | answers_trace.json |
                                             +--------------------+

```
### **Flow Explanation**

1. **User Query** ✨: Input query from user.  
2. **Retriever** 🔍: Searches the KB (FAISS embeddings) for top-k relevant documents.  
3. **Reasoner** 🧠: GPT-4o-mini reads KB context and decides **KB or Tool**.  
4. **KB** 📚: Used directly if Reasoner decides KB is sufficient.  
5. **Actor** 🌐: Tavily web search executed if Reasoner decides KB is insufficient.  
6. **Final Answer** ✅: Generated and returned to user.  
7. **Trace Log** 📝: Step-by-step reasoning, tool calls, and latency logged in `answers_trace.json` and `evaluation.md`.  

---

## 🧩 Project Structure
```
mini_agentic_pipeline/
│
├─ kb_docs/                  # 8–20 text documents (knowledge base)
├─ prompts/                  # External prompt templates (v1, v2)
├─ modules/
│   ├─ retriever.py          # KB vector search
│   ├─ reasoner.py           # LLM reasoning & action decision
│   ├─ actor.py              # Tool integration (Tavily API)
│   └─ controller.py         # Orchestrates the pipeline
├─ answers_trace.json        # Step-by-step trace log
├─ answers.txt               # Final answers per query
├─ evaluation.md             # Automated evaluation report
├─ main.py                   # Entry point for running queries
├─ requirements.txt          # Python dependencies
├─ .env                      # API keys (OpenAI, Tavily)
└─ README.md                 # Documentation

```
---

## ⚙️ Setup Instructions⚡

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd mini_agentic_pipeline
```
2. **Create a virtual environment & install dependencies**

```bash
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows
pip install -r requirements.txt
```
3. **Configure API keys 🔑**

Create a .env file:
```bash
OPENAI_API_KEY=<your_openai_api_key>
TAVILY_API_KEY=<your_tavily_api_key>
```
4. **Add KB documents 📚**
   
```bash
Place 8–20 .txt files in kb_docs/.
```
5.  **Add custom queries and prompt versions**

```bash
Place 8–10 queries in queries.txt
And place prompt versions v1,v2.. as .txt files in promots
```
  
6. **Run the pipeline ▶️**

Default queries:

```bash
python main.py
```

Using a custom queries file and prompt version:
```bash
python main.py --queries-file queries.txt --prompt-version v2
```

## 🛠️ Design Decisions

1. Modular architecture: Retriever, Reasoner, Actor, Controller separated for maintainability.

2. LLM-driven decision-making: GPT-4o-mini chooses whether to use KB or external tool.

3. External prompts: Stored in prompts/ folder for versioning.

4. Trace logging: All queries log retrieved docs, reasoning trace, tool usage, and latency in answers_trace.json.

5. Evaluation report: evaluation.md contains aligned tables, latencies, and quality notes.

6. Agentic Behavior: Decisions made dynamically per query, no fixed thresholds.


## 🖥️ Demo Output

| Query                                     | Decision Text    | Source Used | Latency (s) | Tool Latency (s) |
| ----------------------------------------- | ---------------- | ----------- | ----------- | ---------------- |
| Explain RAG pipeline                      | `action: kb`     | KB          | 4.10        | -                |
| Latest AI research in education           | `action: tavily` | Tavily      | 4.85        | 2.02             |
| Benefits of using embeddings              | `action: tavily` | Tavily      | 6.37        | 2.26             |
| What is FAISS in vector search?           | `action: tavily` | Tavily      | 5.28        | 1.95             |
| When to use web search vs knowledge base? | `action: tavily` | Tavily      | 5.01        | 1.73             |

## Step-by-step trace (from answers_trace.json):

```bash
{
  "query": "Explain RAG pipeline",
  "answer": "Retrieval Augmented Generation (RAG) combines vector search with LLMs...",
  "reasoning_trace": {
    "prompt_version": "v2",
    "used": "KB",
    "decision_text": "action: kb"
  },
  "latency": 4.098,
  "tool_latency": null
}
```
## ⚠️ Known Limitations

-- External API dependency: Tavily API must be accessible; network failures are not retried automatically.

-- Limited KB size: Works best with small KB (8–20 documents).

-- Query coverage: LLM may occasionally misclassify whether to use KB vs tool.

-- No caching: Tool results are fetched on every run; caching could reduce latency.

## 🚀 Future Enhancements

-- Add unit tests for Retriever and Reasoner.

-- Implement retry logic and caching for tool/API calls.

-- Extend to multiple tools (CSV lookup, REST API).

-- Interactive CLI for live queries and optional debugging.
