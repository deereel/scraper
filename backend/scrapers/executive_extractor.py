"""
Executive Name Extractor for BeScraped
Purpose: Extract highest ranking executive names from text content
Author: BeScraped Team
"""

import re
from typing import List, Dict, Optional


class ExecutiveExtractor:
    """Extract executive names from text content."""

    def __init__(self):
        """Initialize executive extractor with common executive titles."""
        # Executive titles in order of hierarchy (UK specific)
        self.executive_titles = [
            'CEO', 'Chief Executive Officer',
            'Founder',
            'Managing Director',
            'Owner',
            'President',
            'Director',
            'Chief Financial Officer', 'CFO',
            'Chief Operating Officer', 'COO',
            'Chief Technology Officer', 'CTO',
            'Vice President', 'VP',
            'General Manager', 'GM',
            'Partner',
            'Head of'
        ]

        # Common name patterns (UK/English names)
        self.name_patterns = [
            re.compile(r'([A-Z][a-zA-Z]+(?:\s[A-Z][a-zA-Z]+)?)', re.IGNORECASE),
            re.compile(r'([A-Z][a-z]+\s[A-Z]\.\s[A-Z][a-z]+)', re.IGNORECASE)
        ]

    def extract_executives(self, text: str) -> List[Dict]:
        """
        Extract executive information from text content.

        Args:
            text: Text content to extract from

        Returns:
            List of executive information with details
        """
        executives = []

        for title in self.executive_titles:
            # Look for patterns like "CEO John Smith" or "John Smith, CEO"
            patterns = [
                re.compile(r'{}[\s:,]*([A-Z][a-zA-Z\s]+)'.format(re.escape(title)), re.IGNORECASE),
                re.compile(r'([A-Z][a-zA-Z\s]+)[\s:,]*{}'.format(re.escape(title)), re.IGNORECASE)
            ]

            for pattern in patterns:
                matches = pattern.findall(text)
                for match in matches:
                    name = self._clean_name(match.strip())
                    if name and len(name.split()) >= 2 and len(name) <= 50:
                        executive = {
                            'name': name,
                            'title': title,
                            'first_name': self._extract_first_name(name),
                            'last_name': self._extract_last_name(name),
                            'confidence': self._calculate_confidence(title)
                        }
                        executives.append(executive)

        # Remove duplicates
        seen = set()
        unique_executives = []
        for executive in executives:
            key = (executive['name'].lower(), executive['title'].lower())
            if key not in seen:
                seen.add(key)
                unique_executives.append(executive)

        return unique_executives

    def _clean_name(self, name: str) -> str:
        """
        Clean extracted name by removing unnecessary characters.

        Args:
            name: Raw extracted name

        Returns:
            Cleaned name
        """
        # Remove punctuation and unnecessary characters
        name = re.sub(r'[^\w\s\-\']', '', name)
        name = re.sub(r'\s+', ' ', name)
        return name.strip()

    def _extract_first_name(self, name: str) -> str:
        """
        Extract first name from full name.

        Args:
            name: Full name

        Returns:
            First name
        """
        parts = name.split()
        return parts[0] if parts else ''

    def _extract_last_name(self, name: str) -> str:
        """
        Extract last name from full name.

        Args:
            name: Full name

        Returns:
            Last name
        """
        parts = name.split()
        return ' '.join(parts[1:]) if len(parts) > 1 else ''

    def _calculate_confidence(self, title: str) -> int:
        """
        Calculate confidence score based on executive title.

        Args:
            title: Executive title

        Returns:
            Confidence score (0-100)
        """
        # CEO and Founder have highest confidence
        if any(keyword in title.lower() for keyword in ['ceo', 'founder']):
            return 95
        elif any(keyword in title.lower() for keyword in ['managing director', 'owner', 'president']):
            return 85
        elif 'director' in title.lower():
            return 80
        elif any(keyword in title.lower() for keyword in ['cfo', 'coo', 'cto']):
            return 75
        elif any(keyword in title.lower() for keyword in ['vice president', 'vp']):
            return 70
        elif any(keyword in title.lower() for keyword in ['general manager', 'partner']):
            return 65
        elif 'head of' in title.lower():
            return 60
        else:
            return 50

    def extract_highest_ranking_executive(self, text: str) -> Optional[Dict]:
        """
        Extract the highest ranking executive from text content.

        Args:
            text: Text content to extract from

        Returns:
            Highest ranking executive information
        """
        executives = self.extract_executives(text)

        if not executives:
            return None

        # Sort by confidence (descending)
        executives.sort(key=lambda x: x['confidence'], reverse=True)

        return executives[0]


def main():
    """Test function."""
    import sys
    if len(sys.argv) != 2:
        print("Usage: python executive_extractor.py <text_file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()

        extractor = ExecutiveExtractor()
        executive = extractor.extract_highest_ranking_executive(text)

        if executive:
            print("Highest ranking executive:")
            print("-" * 50)
            print(f"Name: {executive['name']}")
            print(f"Title: {executive['title']}")
            print(f"First Name: {executive['first_name']}")
            print(f"Last Name: {executive['last_name']}")
            print(f"Confidence: {executive['confidence']}%")
        else:
            print("No executives found in the text.")

    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
