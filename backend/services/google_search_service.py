"""
Google Search Service for BeScraped
Purpose: Search for company information using Serper API
Author: BeScraped Team
"""

import os
import requests
from typing import List, Dict, Optional
from dotenv import load_dotenv

load_dotenv()


class GoogleSearchService:
    """Service to search for company information using Serper API."""

    def __init__(self):
        """Initialize Google Search service with API key from environment variables."""
        self.api_key = os.getenv("SERPER_API_KEY")
        self.base_url = "https://google.serper.dev/search"

    def search(self, query: str, search_type: str = "search") -> Optional[Dict]:
        """
        Perform a Google search using Serper API.

        Args:
            query: Search query
            search_type: Search type (search, images, news, shopping, videos)

        Returns:
            Search results as dictionary
        """
        if not self.api_key:
            print("Serper API key not configured. Search functionality disabled.")
            return None

        headers = {
            "X-API-KEY": self.api_key,
            "Content-Type": "application/json"
        }

        payload = {
            "q": query,
            "type": search_type
        }

        try:
            response = requests.post(self.base_url, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Search failed for query '{query}': {str(e)}")
            return None

    def search_company_info(self, domain: str) -> Dict:
        """
        Search for company information using multiple search queries.

        Args:
            domain: Company domain

        Returns:
            Dictionary of search results from different queries
        """
        results = {
            "domain": domain,
            "queries": {}
        }

        # Search queries to find company information
        queries = [
            f"site:{domain} CEO",
            f"site:{domain} founder",
            f"site:{domain} managing director",
            f"site:linkedin.com {domain} CEO",
            f"{domain} site:find-and-update.company-information.service.gov.uk"
        ]

        for query in queries:
            search_result = self.search(query)
            if search_result:
                results["queries"][query] = search_result

        return results

    def extract_linkedin_profiles(self, search_results: Dict) -> List[Dict]:
        """
        Extract LinkedIn profiles from search results.

        Args:
            search_results: Search results dictionary

        Returns:
            List of LinkedIn profiles with details
        """
        linkedin_profiles = []

        for query, result in search_results.get("queries", {}).items():
            if "linkedin" in query.lower():
                if "organic" in result:
                    for item in result["organic"]:
                        if "linkedin.com/in/" in item.get("link", "") or "linkedin.com/company/" in item.get("link", ""):
                            linkedin_profiles.append({
                                "query": query,
                                "title": item.get("title", ""),
                                "link": item.get("link", ""),
                                "snippet": item.get("snippet", "")
                            })

        return linkedin_profiles

    def extract_companies_house_links(self, search_results: Dict) -> List[Dict]:
        """
        Extract Companies House links from search results.

        Args:
            search_results: Search results dictionary

        Returns:
            List of Companies House links with details
        """
        companies_house_links = []

        for query, result in search_results.get("queries", {}).items():
            if "company-information" in query.lower():
                if "organic" in result:
                    for item in result["organic"]:
                        if "find-and-update.company-information.service.gov.uk" in item.get("link", ""):
                            companies_house_links.append({
                                "query": query,
                                "title": item.get("title", ""),
                                "link": item.get("link", ""),
                                "snippet": item.get("snippet", "")
                            })

        return companies_house_links


def main():
    """Test function."""
    import sys
    if len(sys.argv) != 2:
        print("Usage: python google_search_service.py <domain>")
        sys.exit(1)

    try:
        service = GoogleSearchService()
        domain = sys.argv[1]
        print(f"Searching for company information about {domain}...")
        results = service.search_company_info(domain)

        print("\n--- LinkedIn Profiles ---")
        linkedin_profiles = service.extract_linkedin_profiles(results)
        for profile in linkedin_profiles:
            print(f"- {profile['title']} ({profile['link']})")

        print("\n--- Companies House Links ---")
        companies_house_links = service.extract_companies_house_links(results)
        for link in companies_house_links:
            print(f"- {link['title']} ({link['link']})")

    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
