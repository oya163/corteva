"""
    Author - Oyesh Mann Singh
    Date - 12/27/2022
    Description:
        1. This script loads the YieldData table
        with the yield data file present in code-challenge-template/yld_data.
        2. Creates log file to log the necessary information.
"""

import os
import csv
import logging
from datetime import datetime
from weatherapp.models import YieldData

logging.basicConfig(filename='logs/data_ingestion.log',
                    filemode='a',
                    format='%(asctime)s %(levelname)s:%(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    level=logging.DEBUG)


def run():
    logging.info(
        "=====================YIELD DATA INGESTION STARTED=====================")
    start_time = datetime.now()
    rec_count = 0
    total_count = 0
    for root, _, files in os.walk('code-challenge-template/yld_data'):
        for file in files:
            file_name = os.path.join(root, file)
            with open(file_name, newline='', encoding='utf-8') as csvfile:
                yield_data_list = []
                data = csv.reader(csvfile, delimiter="\t")
                for row in data:
                    total_count += 1
                    yield_data = YieldData(
                        date=datetime.strptime(row[0], '%Y').date(),
                        corn_grain_yield=float(row[1]),
                        created_at=datetime.now())
                    yield_data_list.append(yield_data)
                try:
                    inserted_list = YieldData.objects.bulk_create(
                        yield_data_list)
                    rec_count += len(inserted_list)
                except:  # pylint: disable=W0702
                    logging.warning("Duplicate data insertion not allowed !!!")
                finally:
                    yield_data_list = []

    end_time = datetime.now()

    logging.info("Data ingestion started at: %s", str(start_time))
    logging.info("Data ingestion ended at: %s", str(end_time))
    logging.info("Total number of records found: %s", str(total_count))
    total_time_taken = (end_time-start_time).total_seconds()
    logging.info("Data ingestion took: %s seconds to ingest %s records", str(
        total_time_taken), str(rec_count))
    logging.info(
        "=====================YIELD DATA INGESTION ENDED=====================\n")
