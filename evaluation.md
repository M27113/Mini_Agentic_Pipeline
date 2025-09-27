# Evaluation Report

## Test Queries & Results

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

## Latency Summary
- **Average Latency:** 4.84s
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

