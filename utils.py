"""Modules for utils."""

import csv
import logging
import pyarrow.parquet as pq
from pyarrow import Table
from pathlib import Path
from datetime import datetime as dt
from typing import Dict, List


def get_unique_days(data: List, time_key: str) -> Dict:
    """ Create dictionary with unique date values as keys and empty lists as values.

    :param data: Input table.
    :param time_key: Column name of time.
    """
    unique_list_of_days = [dt.strftime(sub[time_key], "%Y-%m-%d") for sub in data]
    days = sorted(list(set(unique_list_of_days)), key=lambda x: dt.strptime(x, '%Y-%m-%d'))

    u_days = {i: [] for i in days}

    return u_days


def make_dict(csv_file_path):
    """Function to convert a CSV to JSON. Takes the file paths as arguments.

    :param csv_file_path: Path of input csv file.
    """
    # create a dictionary
    data = []

    # Open a csv reader called DictReader
    with open(csv_file_path, encoding='utf-8') as csvf:
        csv_reader = csv.DictReader(csvf)

        # Convert data into a list of dicts
        for rows in csv_reader:
            data.append(rows)

    return data


def read_file(file_name: str):
    """Read File as pandas dataframe.

    :param file_name: Name of the file.
    """
    return pq.read_table(f"{Path(__file__).parent}/data/{file_name}.parquet")


def save_output(file_name: str, data: List) -> None:
    """Save output.

    :param file_name: Name of the file.
    :param data: Data will be written.
    """
    try:
        with open(f"{Path(__file__).parent}/output/{file_name}.csv", "w", newline="") as f:
            w = csv.DictWriter(f, list(data[0].keys()), delimiter=';')
            w.writeheader()
            for i in data:
                print(i)
                w.writerow(i)
            logging.info(f"Output save to {Path(__file__).parent}/output/{file_name}.csv")
    except AttributeError as e:
        logging.error(e)
