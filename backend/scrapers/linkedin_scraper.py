"""
LinkedIn Executive Discovery Service
Purpose: Search for and extract executive information from LinkedIn
Author: BeScraped Team
"""

import os
import requests
from typing import Dict, List, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class LinkedInExecutiveDiscovery:
    """A service to find and extract executive information from LinkedIn."""

    def __init__(self):
        """Initialize the LinkedIn executive discovery service with API key."""
        self.api_key = os.getenv("SERPER_API_KEY")
        self.base_url = "https://google.serper.dev/search"

        if not self.api_key:
            raise ValueError("SERPER_API_KEY not found in environment variables")

    def search_executives(self, company_name: str) -> List[Dict]:
        """
        Search for executive profiles on LinkedIn using company name.

        Args:
            company_name: The name of the company to search for executives.

        Returns:
            A list of executive information dictionaries.
        """
        executives = []

        # Search for company executives using Serper API
        search_queries = [
            f"site:linkedin.com/in {company_name} CEO",
            f"site:linkedin.com/in {company_name} Chief Executive Officer",
            f"site:linkedin.com/in {company_name} Founder",
            f"site:linkedin.com/in {company_name} Managing Director",
            f"site:linkedin.com/in {company_name} Director"
        ]

        for query in search_queries:
            search_results = self._serper_search(query)
            if search_results:
                executives.extend(self._parse_search_results(search_results, company_name))

        return executives

    def _serper_search(self, query: str) -> Optional[Dict]:
        """
        Perform a Google search using Serper API.

        Args:
            query: The search query.

        Returns:
            The search results as a dictionary, or None if search fails.
        """
        headers = {
            "X-API-KEY": self.api_key,
            "Content-Type": "application/json"
        }

        payload = {
            "q": query,
            "type": "search"
        }

        try:
            response = requests.post(self.base_url, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            print(f"Search failed for query '{query}': {str(e)}")
            return None

    def _parse_search_results(self, search_results: Dict, company_name: str) -> List[Dict]:
        """
        Parse search results to extract executive information.

        Args:
            search_results: The search results from Serper API.
            company_name: The company name to validate results.

        Returns:
            A list of parsed executive information dictionaries.
        """
        executives = []

        if "organic" in search_results:
            for item in search_results["organic"]:
                # Skip results that don't contain LinkedIn profiles
                if "linkedin.com/in/" not in item.get("link", ""):
                    continue

                # Extract name from title
                title = item.get("title", "")
                snippet = item.get("snippet", "")

                # Parse executive title (CEO, Founder, etc.)
                executive_title = self._extract_executive_title(title, snippet)
                if not executive_title:
                    continue

                # Extract name from LinkedIn profile URL or title
                name = self._extract_name(title, item.get("link", ""))

                # Validate the result is related to the company
                if company_name.lower() in snippet.lower() or company_name.lower() in title.lower():
                    executives.append({
                        "name": name,
                        "title": executive_title,
                        "link": item.get("link"),
                        "snippet": snippet,
                        "source": "LinkedIn"
                    })

        return executives

    def _extract_executive_title(self, title: str, snippet: str) -> Optional[str]:
        """
        Extract executive title from search result.

        Args:
            title: The search result title.
            snippet: The search result snippet.

        Returns:
            The executive title (CEO, Founder, etc.), or None if not found.
        """
        executive_titles = [
            "CEO", "Chief Executive Officer",
            "Founder", "Co-Founder",
            "Managing Director", "MD",
            "Director", "Chief Executive",
            "President", "VP", "Vice President",
            "COO", "Chief Operating Officer",
            "CFO", "Chief Financial Officer",
            "CTO", "Chief Technology Officer"
        ]

        # Check both title and snippet for executive titles
        combined_text = f"{title} {snippet}"

        for et in executive_titles:
            if et.lower() in combined_text.lower():
                return et

        return None

    def _extract_name(self, title: str, linkedin_url: str) -> str:
        """
        Extract name from LinkedIn profile URL or title.

        Args:
            title: The search result title.
            linkedin_url: The LinkedIn profile URL.

        Returns:
            Extracted name.
        """
        # Try to extract from LinkedIn URL (which typically has the format /in/first-last-123456/)
        import re
        url_match = re.search(r'/in/([^/]+)', linkedin_url)
        if url_match:
            url_name = url_match.group(1)
            # Remove numbers and special characters from URL name
            cleaned = re.sub(r'[0-9-]+$', '', url_name)
            return ' '.join(cleaned.split('-'))

        # Fallback to extract from title
        # Title format usually: "John Doe - CEO at Example Company | LinkedIn"
        parts = title.split(' - ')
        if parts:
            return parts[0].strip()

        return "Unknown"

    def extract_exact_position(self, executive_title: str, company_name: str) -> str:
        """
        Determine the exact executive position based on title and company.

        Args:
            executive_title: The extracted executive title.
            company_name: The company name.

        Returns:
            A more specific position title.
        """
        # This could be extended with more complex logic based on company context
        if executive_title in ["CEO", "Chief Executive Officer"]:
            return "CEO"
        elif executive_title in ["Founder", "Co-Founder"]:
            return "Founder"
        elif executive_title in ["Managing Director", "MD"]:
            return "Managing Director"
        elif executive_title == "Director":
            return "Director"
        elif executive_title == "President":
            return "President"
        elif executive_title in ["VP", "Vice President"]:
            return "Vice President"

        return executive_title


# Test the LinkedIn executive discovery
if __name__ == "__main__":
    try:
        linkedin_scraper = LinkedInExecutiveDiscovery()
        test_company = "example limited"

        print(f"Searching for executives at: {test_company}")
        executives = linkedin_scraper.search_executives(test_company)

        if executives:
            print(f"\nFound {len(executives)} executives:")
            for i, exec in enumerate(executives, 1):
                print(f"{i}. {exec['name']} - {exec['title']}")
                print(f"   LinkedIn: {exec['link']}")
                if exec['snippet']:
                    print(f"   {exec['snippet']}")
                print()
        else:
            print(f"No executives found for '{test_company}'")

    except Exception as e:
        print(f"Error: {str(e)}")
