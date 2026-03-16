"""
Company Name Detector for BeScraped
Purpose: Detect company names from various sources
Author: BeScraped Team
"""

import re
from typing import List, Dict, Optional
from bs4 import BeautifulSoup


class CompanyNameDetector:
    """Detect company names from various sources."""

    def __init__(self):
        """Initialize company name detector with common patterns."""
        # Common company suffixes (UK specific)
        self.company_suffixes = [
            'Limited', 'Ltd', 'Limited Liability Company', 'LLC',
            'Public Limited Company', 'PLC', 'Incorporated', 'Inc',
            'Corporation', 'Corp', 'Company', 'Co'
        ]

        # Patterns for company name detection
        self.name_patterns = [
            re.compile(r'[\w\s\.,&\-]+?(?:Limited|Ltd|LLC|PLC|Incorporated|Inc|Corporation|Corp|Company|Co)\b', re.IGNORECASE),
            re.compile(r'^[\w\s\.,&\-]{2,}$', re.MULTILINE)
        ]

    def extract_from_html_title(self, html_content: str) -> List[str]:
        """
        Extract company name from HTML title tag.

        Args:
            html_content: Raw HTML content

        Returns:
            List of potential company names from title
        """
        names = []

        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            title = soup.title
            if title:
                title_text = title.string.strip() if title.string else ''
                if title_text:
                    # Look for company suffixes in title
                    for suffix in self.company_suffixes:
                        if suffix.lower() in title_text.lower():
                            # Extract everything before possible separators
                            for separator in ['|', '-', '–', '/', '\\']:
                                if separator in title_text:
                                    title_text = title_text.split(separator)[0].strip()
                            names.append(title_text)
                    if not names and len(title_text) < 100:
                        names.append(title_text)
        except Exception:
            pass

        return [name.strip() for name in names if name.strip()]

    def extract_from_meta_tags(self, html_content: str) -> List[str]:
        """
        Extract company name from meta tags (og:site_name, etc.).

        Args:
            html_content: Raw HTML content

        Returns:
            List of potential company names from meta tags
        """
        names = []

        try:
            soup = BeautifulSoup(html_content, 'html.parser')

            # Check og:site_name
            og_site_name = soup.find('meta', property='og:site_name')
            if og_site_name and og_site_name.get('content'):
                names.append(og_site_name['content'].strip())

            # Check twitter:site
            twitter_site = soup.find('meta', property='twitter:site')
            if twitter_site and twitter_site.get('content'):
                content = twitter_site['content'].strip()
                if content.startswith('@'):
                    content = content[1:]
                names.append(content)

            # Check meta name="application-name"
            app_name = soup.find('meta', attrs={'name': 'application-name'})
            if app_name and app_name.get('content'):
                names.append(app_name['content'].strip())

            # Check meta name="description"
            description = soup.find('meta', attrs={'name': 'description'})
            if description and description.get('content'):
                # Extract possible company names from description
                matches = []
                for pattern in self.name_patterns:
                    matches.extend(pattern.findall(description['content']))
                names.extend([match.strip() for match in matches])

        except Exception:
            pass

        return [name for name in names if name and len(name) < 100]

    def extract_from_text(self, text: str) -> List[str]:
        """
        Extract company names from plain text.

        Args:
            text: Plain text content

        Returns:
            List of potential company names from text
        """
        names = []

        for pattern in self.name_patterns:
            matches = pattern.findall(text)
            names.extend([match.strip() for match in matches])

        # Filter out names that are too short or too long
        return [
            name for name in names
            if len(name) >= 2 and len(name) <= 100
        ]

    def detect_company_name(self, html_content: str, text_content: str) -> Optional[Dict]:
        """
        Detect the most confident company name from all sources.

        Args:
            html_content: Raw HTML content
            text_content: Cleaned text content

        Returns:
            Most confident company name with source and confidence
        """
        # Extract from various sources
        title_names = self.extract_from_html_title(html_content)
        meta_names = self.extract_from_meta_tags(html_content)
        text_names = self.extract_from_text(text_content)

        # Collect all candidates with source information
        candidates = []

        for name in title_names:
            candidates.append({
                'name': name,
                'source': 'HTML title',
                'confidence': 85
            })

        for name in meta_names:
            candidates.append({
                'name': name,
                'source': 'Meta tags',
                'confidence': 75
            })

        for name in text_names:
            candidates.append({
                'name': name,
                'source': 'Text content',
                'confidence': 60
            })

        # If no candidates found, try to extract from domain (fallback)
        if not candidates:
            return None

        # Find the most confident candidate
        best_candidate = max(candidates, key=lambda x: x['confidence'])

        # Check for company suffixes to increase confidence
        has_suffix = any(suffix.lower() in best_candidate['name'].lower() for suffix in self.company_suffixes)
        if has_suffix:
            best_candidate['confidence'] += 10

        # Ensure confidence doesn't exceed 100
        best_candidate['confidence'] = min(best_candidate['confidence'], 100)

        return best_candidate


def main():
    """Test function."""
    import sys
    if len(sys.argv) != 2:
        print("Usage: python company_name_detector.py <html_file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()

        from backend.utils.html_cleaner import HTMLTextCleaner
        cleaner = HTMLTextCleaner()
        text_content = cleaner.clean_html(html_content)

        detector = CompanyNameDetector()
        company_name = detector.detect_company_name(html_content, text_content)

        if company_name:
            print("Company name detected:")
            print("-" * 50)
            print(f"Name: {company_name['name']}")
            print(f"Source: {company_name['source']}")
            print(f"Confidence: {company_name['confidence']}%")
        else:
            print("No company name detected.")

    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
