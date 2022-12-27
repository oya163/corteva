import os
import csv
import numpy as np
import logging
import pandas as pd
from datetime import datetime
from weatherapp.models import WeatherData

logging.basicConfig(filename='scripts/log_analysis.log',
                    filemode='a',
                    format='%(asctime)s %(levelname)s:%(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    level=logging.DEBUG)


def run():
    # Import django model table into pandas dataframe
    queryset = WeatherData.objects.values_list(
        "date", "max_temp", "min_temp", "precipitation")
    df = pd.DataFrame(list(queryset), columns=[
                      "date", "max_temp", "min_temp", "precipitation"])

    # Check the dataframe has correct number of records as in the database table
    assert df.shape[0] == WeatherData.objects.count()

    # Convert date column into datetime format
    # This way pandas can perform group_by based on date
    df.loc[:, 'date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')

    print("Number of missing values in max_temp",
          df.loc[df['max_temp'] == -9999].shape[0])

    # Replace -9999 (missing values) with NaN so it is not
    # taken into account while performing aggregation
    df.replace(-9999, np.nan, inplace=True)

    # Assert there are no missing values before aggregation
    assert df.loc[df['max_temp'] == -9999].shape[0] == 0
    assert df.loc[df['min_temp'] == -9999].shape[0] == 0
    assert df.loc[df['precipitation'] == -9999].shape[0] == 0

    df_avg_max_temp = df.groupby(
        df['date'].dt.year).agg(avg_max_temp=('max_temp', 'mean'))
    df_avg_min_temp = df.groupby(
        df['date'].dt.year).agg(avg_min_temp=('min_temp', 'mean'))

    df_sum_precip = df.groupby(df['date'].dt.year).agg(
        total_precip=('precipitation', 'sum'))

    print(df_avg_max_temp.head(10))
    print(df_avg_min_temp.head(10))

    df_sum_precip = df_sum_precip['total_precip'] * 0.01
    print(df_sum_precip.head)
    # print(df_precipitation['sum'] * 0.01)
