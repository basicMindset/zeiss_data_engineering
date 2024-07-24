import logging
import json
from typing import Dict
from pyarrow import Table
from utils import get_unique_days, save_output
from pathlib import Path
from datetime import datetime as dt


def get_decoded_payment_types() -> Dict:
    with open(f"{Path(__file__).parent}/data/payment_types.json") as f:
        data = json.load(f)

    return data


def calc_payment_type_rate(table: Table, file_name_date: str) -> None:
    """Calculate the payment type rate per day.

    :param table: Input pyarrow table.
    :param file_name_date: Date from file name.
    """
    logging.info(f"Calculate payment type rate.")
    reporting_cols = ["tpep_pickup_datetime", "payment_type"]

    payment_types = get_decoded_payment_types()

    # Create subset of data for shortest, longest trip calculations
    subset_data = table.select(reporting_cols).to_pylist()

    unique_days = get_unique_days(data=subset_data, time_key=reporting_cols[0])

    res = []
    for k, v in unique_days.items():
        payments = {"date": k}
        logging.info(f"Current day of iteration: {k}")
        lists_of_payments = [i.get(reporting_cols[1])
                             for i in subset_data
                             if k == dt.strftime(i.get(reporting_cols[0]), "%Y-%m-%d")]
        for identifier, p_type in payment_types.items():
            cnt = lists_of_payments.count(int(identifier))
            length = len(lists_of_payments)
            if cnt != 0:
                pays = {"type": p_type,
                        "total": length,
                        "count": cnt,
                        "rate (%)": f"{str(round((cnt/length)*100, 2))}"}
                payments[f"payments_type_{identifier}"] = pays
                res.append({"date": payments["date"], "payment_type": pays["type"], "rate (%)": pays["rate (%)"]})

    # saving output, because returning the res list will only store last appended value
    # TODO: should be fixed.
    save_output(file_name=f"payment_type_{file_name_date}", data=res)


