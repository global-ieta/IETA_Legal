from .interface import AIProvider
from .prompts import SAFETY_SYSTEM_PROMPT

class MockAuraProvider(AIProvider):
    def intake_conversation(self, message: str) -> str:
        text = (message or "").strip()
        if not text: return "Please describe what happened in your own words. I will ask factual follow-up questions."
        return f"Thank you. I have noted this as user-provided information: ‘{text[:500]}’. What date and location should be associated with it?"
    def summarize_facts(self, facts: str) -> str:
        return f"Factual summary prepared from the information provided: {facts[:1000]}"
