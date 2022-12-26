import os
import csv
import logging
from datetime import datetime
from weatherapp.models import WeatherData

logging.basicConfig(filename='scripts/data_ingestion.log',
                    filemode='a',
                    format='%(asctime)s %(levelname)s:%(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    level=logging.DEBUG)


def run():
    logging.info(
        "===============================DATA INGESTION STARTED===============================")
    start_time = datetime.now()
    rec_count = 0
    for root, dirs, files in os.walk('code-challenge-template/wx_data'):
        for file in files:
            file_name = os.path.join(root, file)
            with open(file_name, newline='', encoding='utf-8') as csvfile:
                weather_data = []
                data = csv.reader(csvfile, delimiter="\t")
                for row in data:
                    rec_count += 1
                    weather = WeatherData(
                        date=datetime.strptime(row[0], '%Y%m%d').date(),
                        max_temp=float(row[1]),
                        min_temp=float(row[2]),
                        precipitation=float(row[3]),
                        created_at=datetime.now())
                    weather_data.append(weather)
            try:
                WeatherData.objects.bulk_create(weather_data)
            except:  # pylint: disable=W0702
                logging.warning("Duplicate data insertion not allowed !!!")
            finally:
                weather_data = []

    end_time = datetime.now()

    logging.info("Data ingestion started at: %s", str(start_time))
    logging.info("Data ingestion ended at: %s", str(end_time))
    logging.info(
        f"Data ingestion took: {(end_time-start_time).total_seconds()} seconds to insert {rec_count} records")
    logging.info(
        "===============================DATA INGESTION ENDED===============================\n")
