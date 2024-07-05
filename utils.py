"""Modules for utils."""

import csv
import logging
from pathlib import Path
import pyarrow.parquet as pq
from typing import List


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
            w = csv.DictWriter(f, list(data[0].keys()))
            w.writeheader()
            for i in data:
                w.writerow(i)
    except AttributeError as e:
        logging.error(e)
