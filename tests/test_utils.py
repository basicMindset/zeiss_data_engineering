import unittest
import datetime
from utils import get_unique_days


class TestUtils(unittest.TestCase):
    def test_get_unique_days(self):
        test_data = [{'tpep_pickup_datetime': datetime.datetime(2009, 1, 1, 23, 58, 40), 'trip_distance': 0.46},
                     {'tpep_pickup_datetime': datetime.datetime(2002, 12, 31, 22, 59, 39), 'trip_distance': 0.63},
                     {'tpep_pickup_datetime': datetime.datetime(2002, 12, 31, 22, 59, 39), 'trip_distance': 0.63},
                     {'tpep_pickup_datetime': datetime.datetime(2009, 1, 1, 23, 30, 39), 'trip_distance': 10.99},
                     {'tpep_pickup_datetime': datetime.datetime(2009, 1, 1, 0, 24, 9), 'trip_distance': 10.88}]
        expected = {'2002-12-31': [],
                    '2009-01-01': []}
        actual = get_unique_days(data=test_data,
                                 time_key="tpep_pickup_datetime")
        self.assertEqual(actual, expected)
