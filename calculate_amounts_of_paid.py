import logging
from typing import Dict, List
from pyarrow import Table
from utils import make_dict, save_output
from pathlib import Path


def get_airports(airport_ids: List) -> Dict:
    """Get airports which are related to the report.

    :param airport_ids: Airport IDs.
    """
    # Read taxi_zone_lookup.csv to decode airport codes
    airport_lookup_list = make_dict(csv_file_path=f"{Path(__file__).parent}/data/taxi_zone_lookup.csv")

    used_airports = {int(j.get("LocationID")): j.get("Zone")
                     for j in airport_lookup_list
                     if int(j.get("LocationID")) in airport_ids}

    return used_airports


def get_total_amount(data: List, cols: List, reporting_airp: Dict, airp: List) -> List:
    """Get total amount for all related airports.

    :param data: Source data.
    :param cols: Report related columns.
    :param reporting_airp: Reporting airports.
    :param airp: Airports.
    """
    airports_amount = {i: [] for i in airp}
    for i in airp:
        for j in data:
            if i == j.get(cols[0]):
                airports_amount[i].append(sum([j.get(cols[1]), j.get(cols[2]), j.get(cols[3])]))

    total = {airport_id: round(sum(amount), 2) for (airport_id, amount) in airports_amount.items()}

    # Replacing ID with Zone names
    final = [
        {"airport_id": i, "airport": zone, "total_amount": tot}
        for i, tot in total.items()
        for j, zone in reporting_airp.items()
        if i == j
    ]

    return final


def calc_amounts_of_paid(table: Table, file_name_date: str) -> None:
    """Calculate the amounts paid (tipAmount, tollsAmount, totalAmount) by airports (rateCodeId).

    :param table: Input pyarrow table.
    :param file_name_date: Date from file name.
    """
    logging.info(f"Calculate total amount for airports.")
    reporting_cols = ["RatecodeID", "tip_amount", "tolls_amount", "total_amount"]

    # Create subset of data for shortest, longest trip calculations
    subset_data = table.select(reporting_cols).to_pylist()

    # In "RatecodeID" column there are a None values, replacing them with 0
    res = [sub[reporting_cols[0]] if sub[reporting_cols[0]] else 0 for sub in subset_data]
    unique_airports = sorted(list(set(res)))
    reporting_airports_zones = get_airports(airport_ids=unique_airports)

    final = get_total_amount(data=subset_data,
                             cols=reporting_cols,
                             reporting_airp=reporting_airports_zones,
                             airp=unique_airports)

    # saving output, because returning the res list will only store last appended value
    # TODO: should be fixed.
    save_output(file_name=f"total_amount_{file_name_date}", data=final)
