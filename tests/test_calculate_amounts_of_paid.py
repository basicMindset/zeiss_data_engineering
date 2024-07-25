import unittest
from scripts.calculate_amounts_of_paid import get_total_amount, get_airports


class TestAmountsOfPaid(unittest.TestCase):
    def test_get_airports(self):
        """Test for getting airports which are related to the report."""
        test_airport_ids = [1, 2]
        expected = {1: 'Newark Airport', 2: 'Jamaica Bay'}
        actual = get_airports(airport_ids=test_airport_ids)

        self.assertEqual(actual, expected)

    def test_get_total_amount(self):
        """Test for getting total amount for all related airports."""
        test_data = [{'RatecodeID': 1, 'tip_amount': 3.42, 'tolls_amount': 0.0, 'total_amount': 20.52},
                     {'RatecodeID': 1, 'tip_amount': 3.0, 'tolls_amount': 0.0, 'total_amount': 29.2},
                     {'RatecodeID': 1, 'tip_amount': 3.55, 'tolls_amount': 0.0, 'total_amount': 21.35},
                     {'RatecodeID': 1, 'tip_amount': 5.24, 'tolls_amount': 0.0, 'total_amount': 31.44},
                     {'RatecodeID': 1, 'tip_amount': 4.82, 'tolls_amount': 0.0, 'total_amount': 28.92},
                     {'RatecodeID': 1, 'tip_amount': 3.0, 'tolls_amount': 0.0, 'total_amount': 15.5},
                     {'RatecodeID': 1, 'tip_amount': 1.0, 'tolls_amount': 0.0, 'total_amount': 20.2},
                     {'RatecodeID': 1, 'tip_amount': 3.98, 'tolls_amount': 0.0, 'total_amount': 23.88},
                     {'RatecodeID': 1, 'tip_amount': 0.0, 'tolls_amount': 6.94, 'total_amount': 43.94},
                     {'RatecodeID': 1, 'tip_amount': 3.14, 'tolls_amount': 0.0, 'total_amount': 18.84},
                     {'RatecodeID': 1, 'tip_amount': 0.0, 'tolls_amount': 0.0, 'total_amount': 26.9},
                     {'RatecodeID': 1, 'tip_amount': 0.0, 'tolls_amount': 0.0, 'total_amount': 21.3}]

        expected = [{'airport_id': 1, 'airport': 'Newark Airport', 'total_amount': 340.08}]

        actual = get_total_amount(data=test_data,
                                  cols=["RatecodeID", "tip_amount", "tolls_amount", "total_amount"],
                                  reporting_airp={1: 'Newark Airport'},
                                  airp=[0, 1, 2, 3, 4, 5, 6, 99])

        self.assertEqual(actual, expected)
