import logging.handlers
import sys
from utils import read_file, save_output
from datetime import datetime as dt
from typing import Dict, List
from pyarrow import Table


def gen_subset_of_data(inp: List) -> Dict:
    """Generator for trip data.

    :param inp: Input data
    """
    for d in inp:
        yield d


def get_min_max(data: List, time_key: str, distance_key: str) -> None:
    """Collect trip distance values per day.

    :param data: Input data.
    :param time_key: Column name contains date info.
    :param distance_key: Column name contains distance values.
    """
    # Create dictionary with unique date values as keys and empty lists as values.
    # Later this dict will be filled up to calculate the shortest and longest distances.
    unique_list_of_days = [dt.strftime(sub[time_key], "%Y-%m-%d") for sub in data]
    days = sorted(list(set(unique_list_of_days)), key=lambda x: dt.strptime(x, '%Y-%m-%d'))

    unique_days = {}
    for i in days:
        unique_days[i] = []

    res = []
    for k, v in unique_days.items():
        min_max = {}
        logging.info(f"Current day of iteration: {k}")
        for i in gen_subset_of_data(inp=data):
            if k == dt.strftime(i.get(time_key), "%Y-%m-%d"):
                unique_days[k].append(i.get(distance_key))
        min_max["date"] = k
        min_max["shortest"] = min(unique_days[k])
        min_max["longest"] = max(unique_days[k])
        res.append(min_max)
        logging.info(f"Entry has been added: {min_max}")

    # saving output, because returning the res list will only store last appended value
    # TODO: should be fixed.
    save_output(file_name="short_long", data=res)


def calculate_shortest_longest(table: Table, time_key: str, distance_key: str):
    """Calculate the shortest and longest (tripDistance) trips by time of day.

    :param table: Table of data.
    :param time_key: Column name contains date info.
    :param distance_key: Column name contains distance values.
    """
    # Create subset of data for shortest, longest trip calculations
    subset_data = table.select([time_key, distance_key]).to_pylist()

    logging.info("Calculating shortest and longest trips per day.")
    # Calculate shortest, longest trips
    get_min_max(data=subset_data,
                time_key=time_key,
                distance_key=distance_key)


if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
    logging.basicConfig(filename='zeiss_logs.log', level=logging.INFO)

    # Input filename
    file_name = "yellow_tripdata_2023-01"
    logging.info(f"Process started at {dt.now()}")
    logging.info(f"Input file: {file_name}")

    # Open a Parquet file and read schema
    data = read_file(file_name)

    # Exercise #1
    calculate_shortest_longest(table=data,
                               time_key='tpep_pickup_datetime',
                               distance_key='trip_distance')
