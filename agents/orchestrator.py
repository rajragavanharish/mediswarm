"""
Orchestrator Agent
Role: The brain. Receives the user question, runs all 3 agents
      in order, handles any errors, and prints the final report.

Flow:
  User Question
       ↓
  Orchestrator
       ↓
  Researcher → Synthesizer → Validator
       ↓
  Final Report
"""

import sys
import os

# This line lets Python find the other agent files
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents import researcher, synthesizer, validator


def thinking_log(message: str):
    print(f"\n  🤖 [Orchestrator] {message}")


def run(query: str) -> dict:
    """Runs all agents in sequence and returns the final report."""

    print("\n" + "="*50)
    print("   MediSwarm — Health Research Swarm")
    print("="*50)
    thinking_log(f"Received question: '{query}'")
    thinking_log("Plan: Researcher → Synthesizer → Validator")

    # ── Step 1: Research ──────────────────────────
    print("\n--- Step 1: Researcher Agent ---")
    try:
        research_data = researcher.run(query)

        # Recovery: if nothing found, try shorter query
        if research_data["source_count"] == 0:
            thinking_log("Nothing found. Trying shorter search...")
            short_query = " ".join(query.split()[:3])
            research_data = researcher.run(short_query)

    except Exception as e:
        thinking_log(f"Researcher failed: {e}. Using fallback.")
        research_data = {"results": [], "source_count": 0, "query": query}

    # ── Step 2: Synthesize ────────────────────────
    print("\n--- Step 2: Synthesizer Agent ---")
    try:
        synthesis_data = synthesizer.run(query, research_data)

    except Exception as e:
        thinking_log(f"Synthesizer failed: {e}")
        synthesis_data = {
            "summary": "Synthesis failed. Please check your GEMINI_API_KEY in the .env file.",
            "sources": research_data.get("results", []),
        }

    # ── Step 3: Validate ──────────────────────────
    print("\n--- Step 3: Validator Agent ---")
    try:
        final_data = validator.run(query, synthesis_data)

    except Exception as e:
        thinking_log(f"Validator failed: {e}")
        final_data = {
            "final_report": synthesis_data["summary"],
            "sources": synthesis_data.get("sources", []),
            "safe": False,
        }

    # ── Print Final Report ────────────────────────
    print("\n" + "="*50)
    print("   FINAL REPORT")
    print("="*50)
    print(final_data["final_report"])
    print("="*50)

    thinking_log(f"Done! {len(final_data.get('sources', []))} sources cited.")

    return final_data


if __name__ == "__main__":
    if len(sys.argv) > 1:
        user_query = " ".join(sys.argv[1:])
    else:
        user_query = input("\nEnter your health question: ").strip()

    run(user_query)