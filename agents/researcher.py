"""
Researcher Agent
Role: Searches trusted medical sources for health information.
"""

import requests
import json


def thinking_log(message: str):
    """Prints a visible 'thinking' trace - required by hackathon rules!"""
    print(f"  🔍 [Researcher] {message}")


def search_pubmed(query: str, max_results: int = 3) -> list:
    """Search PubMed for medical abstracts. Free, no API key needed."""
    thinking_log(f"Searching PubMed for: '{query}'")
    try:
        # Step 1: Get article IDs
        search_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
        params = {
            "db": "pubmed",
            "term": query,
            "retmax": max_results,
            "retmode": "json",
            "sort": "relevance",
        }
        response = requests.get(search_url, params=params, timeout=10)
        ids = response.json()["esearchresult"]["idlist"]

        if not ids:
            thinking_log("No PubMed results found.")
            return []

        # Step 2: Fetch article summaries
        fetch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
        fetch_params = {
            "db": "pubmed",
            "id": ",".join(ids),
            "retmode": "json",
        }
        fetch_response = requests.get(fetch_url, params=fetch_params, timeout=10)
        data = fetch_response.json()["result"]

        results = []
        for uid in ids:
            article = data.get(uid, {})
            results.append({
                "source": "PubMed",
                "title": article.get("title", "No title"),
                "summary": article.get("title", ""),
                "url": f"https://pubmed.ncbi.nlm.nih.gov/{uid}/",
                "year": article.get("pubdate", "")[:4],
            })
            thinking_log(f"  Found: {article.get('title', '')[:60]}...")

        return results

    except Exception as e:
        thinking_log(f"PubMed search failed: {e}")
        return []


def run(query: str) -> dict:
    """Main entry point for the Researcher Agent."""
    thinking_log(f"=== Starting research for: '{query}' ===")

    pubmed_results = search_pubmed(query, max_results=3)

    thinking_log(f"=== Research complete. Found {len(pubmed_results)} sources ===")

    return {
        "agent": "researcher",
        "query": query,
        "results": pubmed_results,
        "source_count": len(pubmed_results),
    }