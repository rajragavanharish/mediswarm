"""
Validator Agent - uses Groq AI (free, fast)
"""

import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

HIGH_RISK_TERMS = [
    "dosage", "dose", "prescription", "overdose",
    "self-medicate", "stop taking", "cure", "guaranteed",
]

DISCLAIMER = """
---
⚕️ MEDICAL DISCLAIMER: This information is for educational purposes only
and does not constitute medical advice. Always consult a qualified
healthcare professional for diagnosis and treatment.
In an emergency, call your local emergency services immediately.
"""


def thinking_log(message: str):
    print(f"  ✅ [Validator] {message}")


def run(query: str, synthesis_data: dict) -> dict:
    thinking_log("=== Starting validation ===")

    summary = synthesis_data.get("summary", "")
    sources = synthesis_data.get("sources", [])

    if not summary:
        thinking_log("WARNING: Empty summary — triggering recovery.")
        return {
            "agent": "validator",
            "query": query,
            "final_report": "Unable to generate a summary. Please try again.",
            "sources": sources,
            "safe": False,
        }

    flagged = [t for t in HIGH_RISK_TERMS if t in summary.lower()]

    if flagged:
        thinking_log(f"⚠️  Flagged terms found: {flagged}")
        thinking_log("Running safety rewrite...")

        api_key = os.getenv("GROQ_API_KEY")
        client = Groq(api_key=api_key)

        safety_prompt = f"""This health summary may contain advice that is too specific.
Please rewrite it to be more general and safe.
Remove any specific dosage or prescription information.
Keep all educational content.

ORIGINAL:
{summary}"""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": safety_prompt}],
        )
        summary = response.choices[0].message.content
        thinking_log("Safety rewrite complete.")
    else:
        thinking_log("No risky content found. Summary is safe ✓")

    final_report = summary + DISCLAIMER

    thinking_log("=== Validation complete. Report is ready! ===")

    return {
        "agent": "validator",
        "query": query,
        "final_report": final_report,
        "sources": sources,
        "safe": True,
    }