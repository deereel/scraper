"""
Company Address Extractor for BeScraped
Purpose: Extract UK company addresses from text content
Author: BeScraped Team
"""

import re
from typing import List, Dict, Optional


class AddressExtractor:
    """Extract company addresses from text content."""

    def __init__(self):
        """Initialize address extractor with UK address patterns."""
        # UK postcode regex pattern
        self.postcode_pattern = re.compile(
            r'([A-Z]{1,2}[0-9]{1,2}[A-Z]?\s?[0-9][A-Z]{2})',
            re.IGNORECASE
        )

        # Street keywords
        self.street_keywords = [
            'street', 'road', 'lane', 'avenue', 'drive', 'court', 'way',
            'street', 'road', 'lane', 'avenue', 'drive', 'court', 'way',
            'place', 'square', 'terrace', 'close', 'gardens', 'estate',
            'parade', 'view', 'hill', 'park', 'green', 'rise', 'vale',
            'common', 'mead', 'brook', 'wood', 'field', 'heath', 'moor',
            'st', 'rd', 'ln', 'ave', 'dr', 'ct', 'wy'
        ]

    def extract_addresses(self, text: str) -> List[Dict]:
        """
        Extract addresses from text content.

        Args:
            text: Text content to extract addresses from

        Returns:
            List of extracted addresses with details
        """
        addresses = []

        # Find all postcodes in the text
        postcodes = list(set(self.postcode_pattern.findall(text)))

        for postcode in postcodes:
            # Find address block containing the postcode
            address_block = self._find_address_block(text, postcode)
            if address_block:
                addresses.append({
                    'address': address_block.strip(),
                    'postcode': postcode.upper(),
                    'confidence': self._calculate_confidence(address_block)
                })

        # Sort addresses by confidence
        addresses.sort(key=lambda x: x['confidence'], reverse=True)

        return addresses

    def _find_address_block(self, text: str, postcode: str) -> Optional[str]:
        """
        Find address block containing a specific postcode.

        Args:
            text: Text content to search in
            postcode: Postcode to find address for

        Returns:
            Address block or None
        """
        # Find the position of the postcode
        postcode_pos = text.find(postcode)
        if postcode_pos == -1:
            return None

        # Look for lines containing street keywords around the postcode
        start_pos = max(0, postcode_pos - 500)
        end_pos = min(len(text), postcode_pos + 500)
        search_window = text[start_pos:end_pos]

        # Split into lines and find address lines
        address_lines = []
        lines = search_window.split('\n')

        for line in lines:
            line = line.strip()
            if postcode in line or any(keyword in line.lower() for keyword in self.street_keywords):
                if len(line) > 5:
                    address_lines.append(line)

        return '\n'.join(address_lines)

    def _calculate_confidence(self, address: str) -> float:
        """
        Calculate confidence score for an extracted address.

        Args:
            address: Extracted address

        Returns:
            Confidence score (0-100)
        """
        score = 0

        # Postcode presence
        if self.postcode_pattern.search(address):
            score += 40

        # Street keywords
        for keyword in self.street_keywords:
            if keyword in address.lower():
                score += 10
                break

        # Number of address components
        lines = address.split('\n')
        score += min(len(lines) * 10, 40)

        # Length of address
        if len(address) > 50:
            score += 10
        elif len(address) < 20:
            score -= 20

        # Ensure score is between 0 and 100
        return max(0, min(100, score))

    def extract_best_address(self, text: str) -> Optional[Dict]:
        """
        Extract the most complete address from text content.

        Args:
            text: Text content to extract address from

        Returns:
            Best address or None
        """
        addresses = self.extract_addresses(text)
        return addresses[0] if addresses else None


def main():
    """Test function."""
    import sys
    if len(sys.argv) != 2:
        print("Usage: python address_extractor.py <text_file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()

        extractor = AddressExtractor()
        address = extractor.extract_best_address(text)

        if address:
            print("Best address found:")
            print("-" * 50)
            print(f"Address: {address['address']}")
            print(f"Postcode: {address['postcode']}")
            print(f"Confidence: {address['confidence']}%")
        else:
            print("No address found in the text.")

    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
