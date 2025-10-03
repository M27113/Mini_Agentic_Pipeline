import os
import sys  
from openai import OpenAI

class Reasoner:
    def __init__(self, prompt_version="v1"):
        try:
            self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            self.prompt_version = prompt_version
            self.prompts_dir = "prompts"
            self.cache = {} # Simple in-memory cache
        except Exception as e:
            print(f"[Error] Failed to initialize Reasoner: {e}")
            sys.exit(1)

    def _load_prompt(self, filename):
        path = os.path.join(self.prompts_dir, filename)
        try:
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            print(f"[Error] Prompt file not found: {path}")
            sys.exit(1)
        except Exception as e:
            print(f"[Error] Failed to load prompt {filename}: {e}")
            sys.exit(1)

    def _get_prompt(self, query, context=""):
        try:
            if self.prompt_version == "v1":
                template = self._load_prompt("v1.txt")
            elif self.prompt_version == "v2":
                template = self._load_prompt("v2.txt")
            else:
                raise ValueError(f"Unsupported prompt version: {self.prompt_version}")
            return template.format(query=query, context=context)
        except Exception as e:
            print(f"[Error] Failed to format prompt: {e}")
            return ""
        
    def reason(self, query, context=""):
        key = (query, context)
        if key in self.cache:  # Check cache first
            return self.cache[key]
        # added try except for better error handling 
        try:
            prompt = self._get_prompt(query, context)
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=250
            )
            output = response.choices[0].message.content.strip()
            self.cache[key] = output  # Cache the result
            return output
        except Exception as e:
            print(f"[Error] LLM reasoning failed: {e}")
            return "LLM reasoning failed due to an error."

    def decide_action(self, query, context=""):
        """
        Decide whether to use KB or external tool (Tavily) based ONLY on LLM decision.
        """
        # added try except for better error handling
        try: 
            context_text = context.get("summary", "") if isinstance(context, dict) else str(context)

            template = self._load_prompt("decide_action.txt")
            prompt = template.format(
                query=query,
                context=context_text if context_text else "No KB context available."
            )

            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=20
            )
            action_text = response.choices[0].message.content.strip().lower()
        except Exception as e:
            print(f"[Error] Failed to decide action: {e}")
            return "error", "Unable to decide action due to an error.", {}
        # LLM decides
        action = "tavily_search" if "tavily" in action_text else "kb_summary"

        # Generate final answer
        answer = self.reason(query, context_text if action == "kb_summary" else "")

        reasoning_trace = {
            "prompt_version": self.prompt_version,
            "used": "KB" if action == "kb_summary" else "Tavily",
            "decision_text": action_text   # log exact LLM output
        }

        return action, answer, reasoning_trace
