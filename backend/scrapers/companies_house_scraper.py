"""
Companies House Scraper
Purpose: Extract company information from the UK Companies House API
Author: BeScraped Team
"""

import os
import requests
from typing import Dict, List, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class CompaniesHouseScraper:
    """A scraper to extract company information from Companies House API."""

    def __init__(self):
        """Initialize the Companies House scraper with API key from environment variables."""
        self.api_key = os.getenv("COMPANIES_HOUSE_API_KEY")
        self.base_url = "https://api.company-information.service.gov.uk"

        if not self.api_key:
            raise ValueError("COMPANIES_HOUSE_API_KEY not found in environment variables")

    def search_company(self, company_name: str) -> Optional[Dict]:
        """
        Search for a company by name.

        Args:
            company_name: The name of the company to search for.

        Returns:
            A dictionary containing company information if found, None otherwise.
        """
        endpoint = f"{self.base_url}/search/companies"
        params = {"q": company_name}

        try:
            response = requests.get(
                endpoint,
                params=params,
                auth=(self.api_key, "")
            )
            response.raise_for_status()
            data = response.json()

            if "items" in data and data["items"]:
                return data["items"][0]  # Return the first matching company

        except requests.exceptions.RequestException as e:
            print(f"Error searching for company '{company_name}': {str(e)}")

        return None

    def get_company_profile(self, company_number: str) -> Optional[Dict]:
        """
        Get detailed company profile from Companies House using company number.

        Args:
            company_number: The Companies House registration number.

        Returns:
            A dictionary containing detailed company information, None otherwise.
        """
        endpoint = f"{self.base_url}/company/{company_number}"

        try:
            response = requests.get(
                endpoint,
                auth=(self.api_key, "")
            )
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            print(f"Error fetching profile for company {company_number}: {str(e)}")

        return None

    def extract_company_info(self, company_data: Dict) -> Dict:
        """
        Extract relevant company information from the API response.

        Args:
            company_data: The raw company data from Companies House API.

        Returns:
            A dictionary containing normalized company information.
        """
        company_info = {
            "company_name": company_data.get("title"),
            "company_number": company_data.get("company_number"),
            "registered_address": self._format_address(company_data.get("address")),
            "company_status": company_data.get("company_status"),
            "incorporation_date": company_data.get("date_of_creation"),
            "company_type": company_data.get("type"),
            "sic_codes": company_data.get("sic_codes", []),
            "uri": company_data.get("uri")
        }

        return company_info

    def _format_address(self, address_data: Optional[Dict]) -> str:
        """
        Format the company address from API data.

        Args:
            address_data: The address data from Companies House API.

        Returns:
            A formatted address string.
        """
        if not address_data:
            return ""

        address_parts = []
        for key in ["premises", "address_line_1", "address_line_2", "locality", "region", "postal_code"]:
            if address_data.get(key):
                address_parts.append(address_data[key])

        return ", ".join(address_parts)

    def search_and_extract(self, company_name: str) -> Optional[Dict]:
        """
        Search for a company and extract detailed information.

        Args:
            company_name: The name of the company to search for.

        Returns:
            A dictionary containing normalized company information, None otherwise.
        """
        search_result = self.search_company(company_name)
        if search_result:
            company_profile = self.get_company_profile(search_result.get("company_number"))
            if company_profile:
                return self.extract_company_info(company_profile)

        return None


# Test the scraper
if __name__ == "__main__":
    try:
        scraper = CompaniesHouseScraper()
        test_company = "example limited"

        print(f"Searching for company: {test_company}")
        company_info = scraper.search_and_extract(test_company)

        if company_info:
            print("\nCompany Information:")
            print(f"Name: {company_info['company_name']}")
            print(f"Number: {company_info['company_number']}")
            print(f"Address: {company_info['registered_address']}")
            print(f"Status: {company_info['company_status']}")
            print(f"Type: {company_info['company_type']}")
            print(f"Incorporation Date: {company_info['incorporation_date']}")

        else:
            print(f"No company found matching '{test_company}'")

    except Exception as e:
        print(f"Error: {str(e)}")
