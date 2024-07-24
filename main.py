import logging
import sys
from calculate_amounts_of_paid import calc_amounts_of_paid
from calculate_shortest_longest import calc_shortest_longest
from calculate_payment_type_rate import calc_payment_type_rate
from utils import read_file


if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    file_handler = logging.FileHandler(filename='zeiss_logs.log')
    stdout_handler = logging.StreamHandler(stream=sys.stdout)
    handlers = [file_handler, stdout_handler]
    logging.basicConfig(level=logging.INFO,
                        format='[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s',
                        handlers=handlers
                        )

    # Input filename
    file_name = "yellow_tripdata_2024-01"
    file_name_date = file_name[16:]
    logging.info(f"Process started")
    logging.info(f"Input file: {file_name}")

    # Open a Parquet file and read schema
    data = read_file(file_name)

    # Exercise #1
    calc_shortest_longest(table=data, file_name_date=file_name_date)

    # Exercise #2
    calc_amounts_of_paid(table=data, file_name_date=file_name_date)

    # Exercise #3
    calc_payment_type_rate(table=data, file_name_date=file_name_date)

    logging.info(f"Data processing finished running")
