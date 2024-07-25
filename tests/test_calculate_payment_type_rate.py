import unittest
import datetime
from scripts.calculate_payment_type_rate import payment_type_rate


class TestCalcPaymentTypeRate(unittest.TestCase):
    def test_payment_type_rate(self):
        """Test for calculating payment rates per day."""
        test_data = [{'tpep_pickup_datetime': datetime.datetime(2023, 12, 31, 23, 56, 46), 'payment_type': 1},
                     {'tpep_pickup_datetime': datetime.datetime(2023, 12, 31, 23, 39, 17), 'payment_type': 1},
                     {'tpep_pickup_datetime': datetime.datetime(2023, 12, 31, 23, 41, 2), 'payment_type': 2},
                     {'tpep_pickup_datetime': datetime.datetime(2023, 12, 31, 23, 57, 17), 'payment_type': 1},
                     {'tpep_pickup_datetime': datetime.datetime(2023, 12, 31, 23, 56, 45), 'payment_type': 1},
                     {'tpep_pickup_datetime': datetime.datetime(2023, 12, 31, 23, 49, 12), 'payment_type': 1},
                     {'tpep_pickup_datetime': datetime.datetime(2023, 12, 31, 23, 47, 28), 'payment_type': 1},
                     {'tpep_pickup_datetime': datetime.datetime(2023, 12, 31, 23, 58, 35), 'payment_type': 2},
                     {'tpep_pickup_datetime': datetime.datetime(2023, 12, 31, 23, 58, 37), 'payment_type': 1},
                     {'tpep_pickup_datetime': datetime.datetime(2023, 12, 31, 23, 54, 27), 'payment_type': 1},
                     {'tpep_pickup_datetime': datetime.datetime(2009, 1, 1, 23, 58, 40), 'payment_type': 2},
                     {'tpep_pickup_datetime': datetime.datetime(2009, 1, 1, 23, 30, 39), 'payment_type': 2},
                     {'tpep_pickup_datetime': datetime.datetime(2009, 1, 1, 0, 24, 9), 'payment_type': 2}]

        test_unique_days = {'2009-01-01': [],
                            '2023-12-31': []}

        test_payment_types = {'1': 'Credit card',
                              '2': 'Cash'}

        expected = [{'date': '2009-01-01', 'payment_type': 'Cash', 'rate (%)': '100.0'},
                    {'date': '2023-12-31', 'payment_type': 'Credit card', 'rate (%)': '80.0'},
                    {'date': '2023-12-31', 'payment_type': 'Cash', 'rate (%)': '20.0'}]
        actual = payment_type_rate(data=test_data,
                                   unique_days=test_unique_days,
                                   reporting_cols=["tpep_pickup_datetime", "payment_type"],
                                   payment_types=test_payment_types,
                                   file_name_date='test',
                                   is_test=True)
        self.assertEqual(actual, expected)
