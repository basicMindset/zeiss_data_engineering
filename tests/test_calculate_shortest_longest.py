import unittest
import datetime
from scripts.calculate_shortest_longest import get_min_max


class TestCalcShortestLongest(unittest.TestCase):
    def test_get_min_max(self):
        """Test for getting min and max values for shortest/longest calculation."""
        test_data = [{'tpep_pickup_datetime': datetime.datetime(2009, 1, 1, 23, 58, 40), 'trip_distance': 0.46},
                     {'tpep_pickup_datetime': datetime.datetime(2002, 12, 31, 22, 59, 39), 'trip_distance': 0.63},
                     {'tpep_pickup_datetime': datetime.datetime(2002, 12, 31, 22, 59, 39), 'trip_distance': 0.63},
                     {'tpep_pickup_datetime': datetime.datetime(2009, 1, 1, 23, 30, 39), 'trip_distance': 10.99},
                     {'tpep_pickup_datetime': datetime.datetime(2009, 1, 1, 0, 24, 9), 'trip_distance': 10.88}]
        expected = [{'date': '2002-12-31', 'shortest': 0.63, 'longest': 0.63},
                    {'date': '2009-01-01', 'shortest': 0.46, 'longest': 10.99}]
        actual = get_min_max(data=test_data,
                             file_name_date='test',
                             cols=["tpep_pickup_datetime", "trip_distance"],
                             is_test=True)
        self.assertEqual(actual, expected)
