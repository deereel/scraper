"""
Google Sheets Importer for BeScraped
Purpose: Import domains from Google Sheets
Author: BeScraped Team
"""

import re
from typing import List, Dict, Optional
from urllib.parse import urlparse, parse_qs
import gspread
from oauth2client.service_account import ServiceAccountCredentials

from backend.utils.domain_normalizer import normalize_domain, validate_domain


class GoogleSheetsImporter:
    """Service to import domains from Google Sheets."""

    def __init__(self, credentials_file: str = "credentials.json"):
        """
        Initialize Google Sheets importer.

        Args:
            credentials_file: Path to Google service account credentials JSON file
        """
        self.credentials_file = credentials_file
        self.credentials = None
        self.client = None

        self._authenticate()

    def _authenticate(self):
        """Authenticate with Google Sheets API using service account credentials."""
        try:
            scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
            self.credentials = ServiceAccountCredentials.from_json_keyfile_name(self.credentials_file, scope)
            self.client = gspread.authorize(self.credentials)
        except Exception as e:
            raise Exception(f"Failed to authenticate with Google Sheets: {str(e)}")

    @staticmethod
    def extract_sheet_id(sheet_url: str) -> Optional[str]:
        """
        Extract Google Sheet ID from URL.

        Args:
            sheet_url: Google Sheet URL

        Returns:
            Sheet ID or None if extraction fails
        """
        # Regex pattern to extract sheet ID from various Google Sheet URL formats
        patterns = [
            r"/spreadsheets/d/([a-zA-Z0-9-_]+)",
            r"key=([a-zA-Z0-9-_]+)"
        ]

        for pattern in patterns:
            match = re.search(pattern, sheet_url)
            if match:
                return match.group(1)

        return None

    def import_domains(self, sheet_url: str) -> List[Dict[str, str]]:
        """
        Import domains from Google Sheet.

        Args:
            sheet_url: Google Sheet URL

        Returns:
            List of normalized domains
        """
        try:
            # Extract sheet ID
            sheet_id = self.extract_sheet_id(sheet_url)
            if not sheet_id:
                raise Exception("Invalid Google Sheet URL")

            # Open the spreadsheet
            spreadsheet = self.client.open_by_key(sheet_id)

            # Get the first worksheet
            worksheet = spreadsheet.sheet1

            # Get all values from the first column
            values = worksheet.col_values(1)

            # Remove duplicates and normalize domains
            seen = set()
            domains = []

            for value in values:
                normalized = normalize_domain(value)
                if normalized and normalized not in seen and validate_domain(normalized):
                    seen.add(normalized)
                    domains.append({"domain": normalized})

            return domains

        except Exception as e:
            raise Exception(f"Failed to import domains from Google Sheet: {str(e)}")


def main():
    """Test function."""
    import sys
    if len(sys.argv) != 2:
        print("Usage: python google_sheets_importer.py <google_sheet_url>")
        sys.exit(1)

    try:
        importer = GoogleSheetsImporter()
        domains = importer.import_domains(sys.argv[1])
        print(f"Successfully imported {len(domains)} domains:")
        for domain in domains:
            print(f"- {domain['domain']}")
    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
