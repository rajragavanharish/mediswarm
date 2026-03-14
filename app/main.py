"""
MediSwarm — Main Entry Point
This is the file you run to start everything.

Usage:
    python app/main.py
"""

import sys
import os

# This lets Python find the agents folder
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.orchestrator import run


def main():
    print("\n╔══════════════════════════════╗")
    print("║      MediSwarm v1.0          ║")
    print("║  AI Health Research Swarm    ║")
    print("╚══════════════════════════════╝")

    print("\nExample questions you can ask:")
    print("  1. What are the symptoms of type 2 diabetes?")
    print("  2. How does high blood pressure affect the heart?")
    print("  3. What is the difference between vitamin D and D3?")

    # Accept question from command line or ask the user
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
        print(f"\nQuestion: {query}")
    else:
        print()
        query = input("Enter your health question: ").strip()

    if not query:
        print("No question provided. Exiting.")
        sys.exit(1)

    run(query)


if __name__ == "__main__":
    main()
