import os
import csv
import logging
from datetime import datetime
from weatherapp.models import WeatherData

# Logging basic configuration
logging.basicConfig(filename='scripts/log_ingestion.log',
                    filemode='w',
                    format='%(asctime)s %(levelname)s:%(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    level=logging.DEBUG)

# Source data directory
WEATHER_DATA_DIR = 'code-challenge-template/wx_data'


def run():
    # To clean up the table
    # WeatherData.objects.all().delete()

    logging.info(
        "=====================WEATHER DATA INGESTION STARTED=====================")
    start_time = datetime.now()
    rec_count = 0
    total_count = 0
    dupli_rec_count = 0
    num_of_files = 0

    # Walk down each files inside a given directory
    for root, dirs, files in os.walk(WEATHER_DATA_DIR):
        for file in files:
            file_name = os.path.join(root, file)
            station_id = file.split('.')[0]     # station id is filename
            weather_data = []
            inserted_list = []
            num_of_files += 1

            # Read each file sequentially
            with open(file_name, newline='', encoding='utf-8') as csvfile:
                data = csv.reader(csvfile, delimiter="\t")
                for row in data:
                    total_count += 1

                    # Prepare weather data for insertion
                    weather = WeatherData(
                        date=datetime.strptime(row[0], '%Y%m%d').date(),
                        max_temp=float(row[1]) if float(
                            row[1]) != -9999 else None,
                        min_temp=float(row[2]) if float(
                            row[2]) != -9999 else None,
                        precipitation=float(
                            row[3]) if float(row[3]) != -9999 else None,
                        station_id=station_id,
                        created_at=datetime.now())

                    # Append each weather data for bulk insertion
                    weather_data.append(weather)

                try:
                    # Bulk insert into database
                    # "ignore_conflicts=True" to ignore conflict
                    # based on duplicate insertion
                    # Returns the number of inserted rows
                    inserted_list = WeatherData.objects.bulk_create(
                        weather_data)
                    rec_count += len(inserted_list)
                    weather_data = []
                except Exception as error:  # pylint: disable=W0702
                    dupli_rec_count += 1
                    logging.error(error)

            logging.info(
                "Number of records ingested from file: %s = %d", file, len(inserted_list))

    end_time = datetime.now()

    # Logging important info
    logging.info("Data ingestion started at: %s", str(start_time))
    logging.info("Data ingestion ended at: %s", str(end_time))
    logging.info("Total number of files processed: %s", num_of_files)
    logging.info("Total number of records found: %s", str(total_count))
    logging.info("Total number of duplicate records found: %s",
                 str(dupli_rec_count))
    total_time_taken = (end_time-start_time).total_seconds()
    logging.info("Data ingestion took: %s seconds to ingest %s records", str(
        total_time_taken), str(rec_count))
    logging.info(
        "=====================WEATHER DATA INGESTION ENDED=====================\n")
