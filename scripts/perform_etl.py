"""
    Author - Oyesh Mann Singh
    Date - 12/27/2022
    Description:
        1. Extracts data from WeatherData table into pandas dataframe
        2. Transforms data using basic data aggregation
        3. Loads the transformed data into the Analytics table
"""

import logging
from datetime import datetime

import numpy as np
import pandas as pd

from weatherapp.models import WeatherData, Analytics

logging.basicConfig(filename='logs/log_etl.log',
                    filemode='a',
                    format='%(asctime)s %(levelname)s:%(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    level=logging.DEBUG)


def perform_aggregation():
    """
        1. Load dataframe from database
        2. Check/Replace missing values
        3. Perform aggregation
        4. Return merged dataframe
    """
    # Import django model table into pandas dataframe
    queryset = WeatherData.objects.values_list(
        "date", "max_temp", "min_temp", "precipitation", "station_id")
    df = pd.DataFrame(list(queryset), columns=[
                      "date", "max_temp", "min_temp", "precipitation", "station_id"])

    # Check the dataframe has correct number of records as in the database table
    assert df.shape[0] == WeatherData.objects.count()

    # Convert date column into datetime format
    # This way pandas can perform group_by based on date
    df.loc[:, 'date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')

    # Check the number of missing values in each column
    logging.info("Number of missing values in max_temp : %d",
                 df.loc[df['max_temp'].isnull()].shape[0])
    logging.info("Number of missing values in min_temp : %d",
                 df.loc[df['min_temp'].isnull()].shape[0])
    logging.info("Number of missing values in precipitation : %d",
                 df.loc[df['precipitation'].isnull()].shape[0])

    # Perform aggregation
    df_avg_max_temp = df.groupby(
        [df['date'].dt.year, 'station_id']).agg(avg_max_temp=('max_temp', 'mean')).reset_index()
    df_avg_min_temp = df.groupby(
        [df['date'].dt.year, 'station_id']).agg(avg_min_temp=('min_temp', 'mean')).reset_index()

    df_sum_precip = df.groupby([df['date'].dt.year, 'station_id']).agg(
        total_precipitation=('precipitation', 'sum')).reset_index()

    # Convert one-tenth of degree Celsius to degree Celsius
    df_avg_max_temp['avg_max_temp'] = df_avg_max_temp['avg_max_temp'] * 0.1
    df_avg_min_temp['avg_min_temp'] = df_avg_min_temp['avg_min_temp'] * 0.1

    # Convert one-tenth of millimeter to centimeter
    df_sum_precip['total_precipitation'] = df_sum_precip['total_precipitation'] * 0.01

    assert df_avg_max_temp.shape[0] == df_avg_min_temp.shape[0]
    assert df_avg_max_temp.shape[0] == df_sum_precip.shape[0]

    # Merge all dataframes based on 'date' and 'station_id'
    final_df = df_avg_max_temp.merge(df_avg_min_temp, on=['date', 'station_id']).merge(
        df_sum_precip, on=['date', 'station_id'])

    assert df_sum_precip.shape[0] == final_df.shape[0]

    return final_df


def run():
    # Analytics table clean up
    # Uncomment when necessary
    # Analytics.objects.all().delete()

    start_time = datetime.now()

    logging.info(
        "=====================ETL STARTED=====================")

    # Get the dataframe after performing required calculation
    df = perform_aggregation()

    # Replace NaNs with Null so PostgreSQL can understand
    df = df.replace(np.nan, None)
    df_with_nulls = df[df.isna().any(axis=1)]

    # Convert dataframe to list of dictionaries of records
    df_records = df.to_dict('records')

    analysis_list = [Analytics(
        date=datetime.strptime(str(row['date']), '%Y').date(),
        avg_max_temp=row['avg_max_temp'],
        avg_min_temp=row['avg_min_temp'],
        total_precipitation=row['total_precipitation'],
        station_id=row['station_id'],
        created_at=datetime.now()) for row in df_records]

    inserted_list = []
    try:
        inserted_list = Analytics.objects.bulk_create(analysis_list)
    except Exception as error:  # pylint: disable=W0702
        logging.error(error)

    end_time = datetime.now()

    # Logging important info
    logging.info("ETL started at: %s", str(start_time))
    logging.info("ETL ended at: %s", str(end_time))
    logging.info(
        "Number of rows with NaN values in Analytics model: %d", df_with_nulls.shape[0])
    logging.info("ETL took: %d seconds and inserted %d records",
                 (end_time-start_time).total_seconds(), len(inserted_list))

    logging.info(
        "=====================ETL ENDED=====================\n")
