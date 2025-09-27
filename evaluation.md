# Evaluation Report

## Test Queries & Results

| Query                                                       | Decision Text    | Source Used | Latency (s) | Tool Latency (s) |
|-------------------------------------------------------------|------------------|-------------|-------------|------------------|
| Explain RAG                                                 | `action: kb`     | KB          | 4.85        | -                |
| What are chatbots?                                          | `action: kb`     | KB          | 2.79        | -                |
| Explain about AI Ethics                                     | `action: kb`     | KB          | 3.37        | -                |
| How does FAISS help in similarity search?                   | `action: tavily` | Tavily      | 5.21        | 2.37             |
| Describe AI applications in healthcare                      | `action: kb`     | KB          | 3.20        | -                |
| What is the role of automation tools like N8N in workflows? | `action: kb`     | KB          | 3.38        | -                |
| Who won the Nobel Prize in Physics 2024?                    | `action: tavily` | Tavily      | 5.51        | 2.65             |
| Current price of Tesla stock                                | `action: tavily` | Tavily      | 4.31        | 1.88             |
| What are some popular Python libraries for NLP?             | `action: kb`     | KB          | 2.58        | -                |
| Upcoming AI conferences worldwide                           | `action: tavily` | Tavily      | 5.27        | 2.25             |

---

## Latency Summary
- **Average Latency:** 4.05s
- **Average Tool Latency:** 2.29s
- **KB Used:** 6 times
- **Web Search Used:** 4 times

---

## Quality Notes
- Most conceptual/technical queries were correctly handled using KB retrieval.
- Web search was correctly chosen for fact-based or recent information.
- Overall latency is slightly high; consider optimizing retrieval or model calls.

---

## Overall Assessment
✅ Transparent decision-making using LLM-only logic.  
✅ Balanced usage between KB and Web search.  
✅ Step-by-step trace logging complete and clear.  
✅ Answers are concise, relevant, and within 3–4 lines.  

