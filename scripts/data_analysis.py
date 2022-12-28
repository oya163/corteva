import logging
from datetime import datetime

import numpy as np
import pandas as pd

from weatherapp.models import WeatherData, Analytics

logging.basicConfig(filename='scripts/log_analysis.log',
                    filemode='a',
                    format='%(asctime)s %(levelname)s:%(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    level=logging.DEBUG)


def perform_analysis():
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

    # Replace None (missing values) with NaN so it is not
    # taken into account while performing aggregation
    # df.replace(None, np.nan, inplace=True)

    # Assert there are no missing values before aggregation
    # assert df.loc[df['max_temp'].isnull()].shape[0] == 0
    # assert df.loc[df['min_temp'].isnull()].shape[0] == 0
    # assert df.loc[df['precipitation'].isnull()].shape[0] == 0

    # Perform aggregation
    df_avg_max_temp = df.groupby(
        [df['date'].dt.year, 'station_id']).agg(avg_max_temp=('max_temp', 'mean')).reset_index()
    df_avg_min_temp = df.groupby(
        [df['date'].dt.year, 'station_id']).agg(avg_min_temp=('min_temp', 'mean')).reset_index()

    df_sum_precip = df.groupby([df['date'].dt.year, 'station_id']).agg(
        total_precipitation=('precipitation', 'sum')).reset_index()

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
    start_time = datetime.now()

    # Analytics table clean up
    # Analytics.objects.all().delete()

    logging.info(
        "=====================DATA ANALYSIS STARTED=====================")

    # Get the dataframe after performing required calculation
    df = perform_analysis()

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
    inserted_list = Analytics.objects.bulk_create(analysis_list)

    end_time = datetime.now()

    # Logging important info
    logging.info("Data analysis started at: %s", str(start_time))
    logging.info("Data analysis ended at: %s", str(end_time))
    logging.info(
        "Number of rows with NaN values in Analytics model: %d", df_with_nulls.shape[0])
    logging.info("Data analysis took: %d seconds and inserted %d records",
                 (end_time-start_time).total_seconds(), len(inserted_list))

    logging.info(
        "=====================DATA ANALYSIS ENDED=====================\n")
