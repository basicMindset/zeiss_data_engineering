import logging
from datetime import datetime as dt
from pyarrow import Table
from typing import List
from utils import save_output


def get_min_max(data: List, file_name: str, time_key: str, distance_key: str) -> None:
    """Collect trip distance values per day.

    :param data: Input data.
    :param file_name: Input file name.
    :param time_key: Column name contains date info.
    :param distance_key: Column name contains distance values.
    """
    # Create dictionary with unique date values as keys and empty lists as values.
    # Later this dict will be filled up to calculate the shortest and longest distances.
    unique_list_of_days = [dt.strftime(sub[time_key], "%Y-%m-%d") for sub in data]
    days = sorted(list(set(unique_list_of_days)), key=lambda x: dt.strptime(x, '%Y-%m-%d'))

    unique_days = {i: [] for i in days}

    res = []
    for k, v in unique_days.items():
        min_max = {}
        logging.info(f"Current day of iteration: {k}")
        for i in data:
            if k == dt.strftime(i.get(time_key), "%Y-%m-%d"):
                unique_days[k].append(i.get(distance_key))
        min_max["date"] = k
        min_max["shortest"] = min(unique_days[k])
        min_max["longest"] = max(unique_days[k])
        res.append(min_max)
        logging.info(f"Entry has been added: {min_max}")

    # saving output, because returning the res list will only store last appended value
    # TODO: should be fixed.
    save_output(file_name=f"short_long_{file_name[16:]}", data=res)


def calc_shortest_longest(table: Table, file_name: str, time_key: str, distance_key: str):
    """Calculate the shortest and longest (tripDistance) trips by time of day.

    :param table: Table of data.
    :param file_name: Input file name.
    :param time_key: Column name contains date info.
    :param distance_key: Column name contains distance values.
    """
    # Create subset of data for shortest, longest trip calculations
    subset_data = table.select([time_key, distance_key]).to_pylist()

    logging.info("Calculating shortest and longest trips per day.")
    # Calculate shortest, longest trips
    get_min_max(data=subset_data,
                file_name=file_name,
                time_key=time_key,
                distance_key=distance_key)
