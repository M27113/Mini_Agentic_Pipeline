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
+-----------+     +--------------------+     +--------------------+     +-----------+     +-------------+
| User Query| --> |     Retriever      | --> |     Reasoner       | --> |    KB     | --> | Final Answer|
+-----------+     |  (FAISS + KB docs) |     | (LLM decides: KB   |     +-----------+     +-------------+
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
7. **Trace Log** 📝: Step-by-step reasoning, tool calls, and latency logged in `answers_trace.json` (raw logs) and summarized in `evaluation.md` (clean tables).  
 

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
├─ generate_eval.py  
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

    Place 8–20 .txt files in kb_docs/.

5. **Add test queries in queries.txt**.

    (1 query per line, 10 queries recommended)
    Place 8–10 queries in queries.txt

6. **Add prompts**

    And place prompt versions v1,v2.. as .txt files in prompts

7. **Run the pipeline**

    i) Default queries:

    ```bash
    python main.py
    ```

    ii) Using a custom queries file and prompt version:
    
    ```bash
    python main.py --queries-file queries.txt --prompt-version v2
    ```
    - queries-file: Path to your queries file.
    
    - prompt-version: Choose between v1 (basic) or v2 (expert) prompt.
    
    **output**:
    
    - answers.txt – readable answers per query.
    
    - answers_trace.json – full JSON with reasoning trace, action decisions, and latencies.

---
## 📌 Design Decisions

These choices were made to keep the pipeline **simple, explainable, and extensible** while meeting the assignment requirements.  

1. **Modular architecture** → Retriever, Reasoner, Actor, and Controller are separated into distinct components for clarity and maintainability.  
2. **LLM-driven decision-making** → GPT-4o-mini decides dynamically whether to use the KB or the external Tavily tool.  
3. **Versioned prompts** → Prompts are stored in the `prompts/` folder, making it easy to maintain and switch between versions.  
4. **Structured trace logging** → Each query logs retrieved docs, reasoning trace, tool usage, and latency in `answers_trace.json` (raw logs), summarized in `evaluation.md` (clean tables).
5. **Evaluation framework** → A dedicated `evaluation.md` provides clean tables with per-query latencies and qualitative notes.  
6. **Agentic behavior** → The pipeline behaves like a lightweight agent, reasoning and acting per query rather than following static rules.  
---
## 📊 Evaluation

1. Queries tested: 10 queries covering RAG, embeddings, FAISS, ML basics, chatbots, AI applications.

2. Metrics captured:

    - overall_latency

    - tool_latency

    - decision_text (action chosen)

3. All raw metrics are stored in answers_trace.json, while evaluation.md presents them in human-readable tables.
---
## 🖥️ Demo Output

**Files Generated:**  
- 📄 [answers.txt](answers.txt) – file contains truncated, human-readable answers for each query 
- 📝 [answers_trace.json](answers_trace.json) – raw logs with full reasoning trace, tool calls,action decisions, and latencies  
- 📊 [evaluation.md](evaluation.md) – summarized tables for easy grading

### Test Queries & Results

**answers.txt:**
> The following snippet shows shows entries from [answers.txt](answers.txt)
```bash
--- Query 1: Explain RAG ---
Answer: RAG can be applied in multiple domains, including customer support, research summarization, healthcare, and finance. It enables AI agents to answer queries about domain-specific documents, such as reports, papers, or knowledge articles. By combining retrieval and generation, RAG systems offer both flexibility and reliability...

(used: KB, latency: 4.85s)

--- Query 2: What are chatbots? ---
Answer: Chatbots are AI systems designed to interact with users through text or voice. They can answer FAQs, assist with customer support, and integrate with workflows. Advanced chatbots leverage LLMs to provide context-aware responses...

(used: KB, latency: 2.79s)

...

```
**Step-by-step trace (from answers_trace.json):**

> The following snippet shows entries from [answers_trace.json](answers_trace.json) (raw logs).

```bash
    {
        "query": "Explain about AI Ethics",
        "answer": "AI Ethics is a critical field that addresses the responsible development and deployment of artificial intelligence. Key principles include fairness, transparency, accountability, privacy, and avoiding bias in AI systems. Ensuring that AI models do not discriminate against individuals or groups is essential for trust and societal acceptance.\n\nTransparency involves explaining AI decisions in a way humans can understand. Accountability ensures that developers and organizations take responsibility...",
        "reasoning_trace": {
            "prompt_version": "v2",
            "used": "KB",
            "decision_text": "action: kb"
        },
        "latency": 3.3738651275634766,
        "tool_latency": null
    },
    {
        "query": "How does FAISS help in similarity search?",
        "answer": "Faiss is an open-source library designed for efficient similarity search and clustering of dense vectors, enabling applications like recommendation systems and image search. Faiss, short for Facebook AI Similarity Search, is an open-source library built for similarity search and clustering of dense vectors. These methods help Faiss organize and retrieve vectors efficiently, ensuring similarity searches are quick and accurate. Faiss also powers search engines that retrieve visually similar...",
        "reasoning_trace": {
            "prompt_version": "v2",
            "used": "Tavily",
            "decision_text": "action: tavily"
        },
        "latency": 5.209009647369385,
        "tool_latency": 2.369060754776001
    }
    ...
```
---
> Full evaluation is summarized in [evaluation.md](evaluation.md).

| Query                                                       | Decision Text    | Source Used | Latency (s) | Tool Latency (s) |
|-------------------------------------------------------------|------------------|-------------|-------------|------------------|
| Explain RAG                                                 | `action: kb`     | KB          | 5.78        | -                |
| What are chatbots?                                          | `action: kb`     | KB          | 4.95        | -                |
| Explain about AI Ethics                                     | `action: kb`     | KB          | 5.66        | -                |
| How does FAISS help in similarity search?                   | `action: tavily` | Tavily      | 5.04        | 2.05             |
| Describe AI applications in healthcare                      | `action: kb`     | KB          | 4.22        | -                |
| What is the role of automation tools like N8N in workflows? | `action: kb`     | KB          | 2.95        | -                |
| Who won the Nobel Prize in Physics 2024?                    | `action: tavily` | Tavily      | 5.63        | 2.64             |
| Current price of Tesla stock                                | `action: tavily` | Tavily      | 5.09        | 2.47             |
| What are some popular Python libraries for NLP?             | `action: kb`     | KB          | 3.91        | -                |
| Upcoming AI conferences worldwide                           | `action: tavily` | Tavily      | 5.14        | 1.99             |

---

### Latency Summary
- **Average Latency:** 4.84s
- **Average Tool Latency:** 2.29s
- **KB Used:** 6 times
- **Web Search Used:** 4 times

---

## ⚠️ Known Limitations
- 🌐 **External API dependency** → Tavily API must be accessible; network failures are not retried automatically.  
- 📚 **Limited KB size** → Optimized for a small knowledge base (8–20 documents).  
- 🤖 **Query coverage** → The LLM may occasionally misclassify whether to use the KB or the tool.  
- ⏳ **No caching** → Tool results are fetched on every run; caching could reduce latency.  

## 🚀 Future Enhancements
- 🧪 Add **unit tests** for Retriever and Reasoner.  
- ♻️ Implement **retry logic and caching** for tool/API calls.  
- 🔧 Extend to support **multiple tools** (e.g., CSV lookup, REST API).  
- 💻 Provide an **interactive CLI** for live queries and optional debugging.  
---
