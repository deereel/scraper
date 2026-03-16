"""
Data Confidence Scoring Engine for BeScraped
Purpose: Rank sources by reliability and calculate confidence scores
Author: BeScraped Team
"""

from typing import Dict, Optional


class ConfidenceScorer:
    """Engine to calculate confidence scores for scraped data based on source reliability."""

    def __init__(self):
        """Initialize confidence scorer with predefined source weights."""
        # Source reliability scores (0-100)
        self.source_scores = {
            'Companies House': 95,
            'LinkedIn': 85,
            'Company Website': 70,
            'Google Snippet': 60,
            'Other': 50
        }

        # Field-specific weights (how important each field is to overall score)
        self.field_weights = {
            'company_name': 0.4,
            'address': 0.3,
            'executive_first_name': 0.15,
            'executive_last_name': 0.15
        }

    def get_source_score(self, source: str) -> int:
        """
        Get score for a specific source.

        Args:
            source: Source name

        Returns:
            Confidence score (0-100)
        """
        for known_source, score in self.source_scores.items():
            if known_source.lower() in source.lower():
                return score

        return self.source_scores['Other']

    def calculate_field_score(self, field_value: Optional[str], source_score: int) -> float:
        """
        Calculate confidence score for a specific field.

        Args:
            field_value: Field value (None if missing)
            source_score: Source reliability score

        Returns:
            Field confidence score (0-100)
        """
        if field_value is None or field_value.strip() == '':
            return 0.0

        # Base score is source score
        score = source_score

        # Adjust based on field value quality
        value_length = len(field_value.strip())
        if value_length < 3:
            score *= 0.3
        elif value_length < 10:
            score *= 0.7
        elif value_length > 200:
            score *= 0.8

        return min(100.0, max(0.0, score))

    def calculate_overall_score(self, record: Dict) -> float:
        """
        Calculate overall confidence score for a complete record.

        Args:
            record: Scraped data record

        Returns:
            Overall confidence score (0-100)
        """
        source_score = self.get_source_score(record.get('source', 'Other'))
        total_score = 0.0

        for field, weight in self.field_weights.items():
            field_value = record.get(field)
            field_score = self.calculate_field_score(field_value, source_score)
            total_score += field_score * weight

        return round(total_score, 2)

    def rank_records_by_confidence(self, records: list) -> list:
        """
        Rank records by overall confidence score.

        Args:
            records: List of scraped data records

        Returns:
            Sorted list of records by confidence (descending)
        """
        # Calculate confidence score for each record
        records_with_scores = []
        for record in records:
            record_with_score = record.copy()
            record_with_score['confidence'] = self.calculate_overall_score(record)
            records_with_scores.append(record_with_score)

        # Sort by confidence descending
        records_with_scores.sort(key=lambda x: x['confidence'], reverse=True)

        return records_with_scores

    def select_best_record(self, records: list) -> Optional[Dict]:
        """
        Select the best record based on confidence score.

        Args:
            records: List of scraped data records

        Returns:
            Best record or None if no records
        """
        if not records:
            return None

        ranked_records = self.rank_records_by_confidence(records)
        return ranked_records[0]


def main():
    """Test function."""
    test_records = [
        {
            'domain': 'example.com',
            'company_name': 'Example Limited',
            'address': '123 Main Street, London, SW1A 1AA',
            'executive_first_name': 'John',
            'executive_last_name': 'Smith',
            'source': 'Companies House'
        },
        {
            'domain': 'example.com',
            'company_name': 'Example Ltd',
            'address': '123 Main St, London',
            'executive_first_name': 'John',
            'executive_last_name': 'Smith',
            'source': 'Company Website'
        },
        {
            'domain': 'example.com',
            'company_name': 'Example Ltd',
            'address': None,
            'executive_first_name': 'John',
            'executive_last_name': 'Smith',
            'source': 'Google Snippet'
        }
    ]

    scorer = ConfidenceScorer()

    print("Ranked records by confidence:")
    print("-" * 80)

    ranked_records = scorer.rank_records_by_confidence(test_records)
    for i, record in enumerate(ranked_records, 1):
        print(f"{i}. {record['company_name']} ({record['source']}) - {record['confidence']}%")
        print(f"   Address: {record['address']}")
        print(f"   Executive: {record['executive_first_name']} {record['executive_last_name']}")
        print()

    best_record = scorer.select_best_record(test_records)
    print("Best record:")
    print("-" * 50)
    print(f"{best_record['company_name']} ({best_record['source']}) - {best_record['confidence']}%")


if __name__ == "__main__":
    main()
