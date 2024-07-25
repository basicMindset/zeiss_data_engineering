import logging
from datetime import datetime as dt
from pyarrow import Table
from typing import Dict, List, Union
from utils import save_output, get_unique_days


def get_min_max(data: List, days: Dict, file_name_date: str, cols: List, is_test: bool) -> Union[List, None]:
    """Collect trip distance values per day.

    :param data: Input data.
    :param days: Dictionary of unique days.
    :param file_name_date: Date from file name.
    :param cols: Reporting columns.
    :param is_test: Differentiate test from actual run.
    """
    res = [
        {
            "date": k,
            "shortest": min(v),
            "longest": max(v)
        }
        for k, v in days.items()
        if (
            logging.info(f"Current day of iteration: {k}") or True,
            [v.append(i.get(cols[1])) for i in data if k == dt.strftime(i.get(cols[0]), "%Y-%m-%d")]
        )
    ]
    if not is_test:
        save_output(file_name=f"payment_type_{file_name_date}", data=res)
    else:
        return res


def calc_shortest_longest(table: Table, file_name_date: str, is_test: bool) -> None:
    """Calculate the shortest and longest (tripDistance) trips by time of day.

    :param table: Table of data.
    :param file_name_date: Date from file name.
    :param is_test: Differentiate test from actual run.
    """
    logging.info("Calculating shortest and longest trips per day.")
    reporting_cols = ["tpep_pickup_datetime", "trip_distance"]

    # Create subset of data for shortest, longest trip calculations
    subset_data = table.select(reporting_cols).to_pylist()
    unique_days = get_unique_days(data=subset_data, time_key=reporting_cols[0])

    # Calculate shortest, longest trips
    get_min_max(data=subset_data,
                days=unique_days,
                file_name_date=file_name_date,
                cols=reporting_cols,
                is_test=is_test)
