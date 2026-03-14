"""
Synthesizer Agent - uses Groq AI (free, fast)
"""

import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()


def thinking_log(message: str):
    print(f"  🧠 [Synthesizer] {message}")


def run(query: str, research_data: dict) -> dict:
    thinking_log("=== Starting synthesis ===")

    results = research_data.get("results", [])

    if not results:
        thinking_log("No research results to synthesize!")
        return {
            "agent": "synthesizer",
            "query": query,
            "summary": "No information found. Please try rephrasing.",
            "sources": [],
        }

    thinking_log(f"Synthesizing {len(results)} sources using Groq AI...")

    sources_text = ""
    for i, item in enumerate(results, 1):
        sources_text += (
            f"\nSource {i} [{item['source']}]: {item['title']}\n"
            f"  URL: {item.get('url', 'N/A')}\n"
        )

    prompt = f"""You are a medical information synthesizer.
Combine the following research results into a clear health summary.

USER QUESTION: {query}

RESEARCH FINDINGS:
{sources_text}

Produce a structured summary with:
1. OVERVIEW - 2 to 3 simple sentences
2. KEY FACTS - 3 to 5 bullet points
3. SOURCES - list each source with URL

Write in plain English. Do NOT give personal medical advice."""

    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY not found! Check your .env file.")

    client = Groq(api_key=api_key)

    thinking_log("Sending to Groq AI for synthesis...")
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
    )
    summary_text = response.choices[0].message.content
    thinking_log("Synthesis complete.")

    sources = [
        {"title": r["title"], "url": r["url"], "source": r["source"]}
        for r in results
    ]

    return {
        "agent": "synthesizer",
        "query": query,
        "summary": summary_text,
        "sources": sources,
        "source_count": len(sources),
    }