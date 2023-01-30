# Corteva Coding Assignment

This is a simple ETL pipeline project

## Tech Stack
```
Backend - Django/Django Rest Framework
Database - PostgreSQL
```

## Installation

### Install postgresql
```
$ sudo apt install postgresql postgresql-contrib
$ sudo -u postgres createuser <username>
$ sudo -u postgres createdb corteva
$ sudo su - postgres
$ psql
$ ALTER USER <username> WITH ENCRYPTED PASSWORD '<password>';
$ GRANT ALL PRIVILEGES ON DATABASE corteva TO <username>;
```

### Install pgadmin (Optional)

Download pgadmin installer from [here](https://www.pgadmin.org/download/pgadmin-4-windows/)


### Install requirements and clone raw data
```
$ python3 -m venv corteva
$ cd corteva
$ source ./bin/activate
$ git clone https://github.com/oya163/corteva.git
$ cd corteva
$ pip install -r requirements.txt
$ git clone https://github.com/corteva/code-challenge-template.git
```


## Folder Structure
```
├── code-challenge-template -> contains the raw data files
│   ├── wx_data
│   └── yld_data
├── manage.py
├── README.md
├── requirements.txt
├── scripts -> contains scripts to load the database, perform analysis and log files
├── weather -> contains django-admin setting for this project
└── weatherapp -> contains django app
```

## How to run

### Data ingestion scripts
 - Weather data ingestion
   - **weather_data_ingestion** script loads the weather data from CSV file and ingests into **WeatherData** table. 
   - Performs basic data cleaning before inserting into database table, like converting -9999 as NULL values, so that it will be easier for calculation in later phases. 
   - Performs bulk insertion of data of each file for faster data ingestion. 
   - Produces log which are recorded into **logs/log_ingestion.log** file.


```
python manage.py runscript weather_data_ingestion
```


 - Yield data ingestion
   - **yield_data_ingestion** script loads the yield data from CSV file and ingests into **YieldData** table. 
   - Produces log which are recorded into **logs/log_ingestion.log** file.
    
```
python manage.py runscript yield_data_ingestion
```


 - Perform ETL
   - **perform_etl** script basically loads the weather data from **WeatherData** table into pandas dataframe.
   - Performs basic calculation like converting temperatures from one-tenths of degree Celsius to degree Celsius and converting precipitation from one-tenths of millimeter into centimeter, and inserts transformed records into **Analytics** table for further consumption by REST API.
   - Produces log which are recorded into **logs/log_etl.log** file.

```
python manage.py runscript perform_etl
```

### Django standalone server

The server is hosted at http://127.0.0.1:8000/ by default

    python manage.py runserver

## REST API

Django Rest Framework's **ListAPIView** and **DjangoFilterBackend** is extensively used to process the GET requests and filter the results according to the query parameters.
Three main APIs are exposed which are explained as follows:-
 - /api/weather
```
This API lists the weather data from WeatherData table.

Query Params (optional):-
    - id(int): record id
    - date(date): record date [format: %Y-%m-%d]
    - station_id(char): weather station id
    - page(int): page number for pagination purpose

Usage:
    - http://127.0.0.1:8000/api/weather?id=5518560
    - http://127.0.0.1:8000/api/weather?page=1
    - http://127.0.0.1:8000/api/weather?date=2014-01-01
    - http://127.0.0.1:8000/api/weather?station_id=USC00110072
    - http://127.0.0.1:8000/api/weather?date=2014-01-01&station_id=USC00110072
``` 

 - /api/yield
```
This API lists the yield data from YieldData table.

Query Params (optional):-
    - id(int): record id
    - date(date): record date [format: %Y-%m-%d]
    - page(int): page number for pagination purpose

Usage:
    - http://127.0.0.1:8000/api/yield?id=1
    - http://127.0.0.1:8000/api/yield?page=1
    - http://127.0.0.1:8000/api/yield?date=2014-01-01
``` 

 - /api/weather/stats
```
This API lists the transformed data from Analytics table.

Query Params (optional):-
    - id(int): record id
    - date(date): record date [format: %Y-%m-%d]
    - station_id(char): weather station id
    - page(int): page number for pagination purpose

Usage:
    - http://127.0.0.1:8000/api/weather/stats?id=1
    - http://127.0.0.1:8000/api/weather/stats?page=1
    - http://127.0.0.1:8000/api/weather/stats?date=2014-01-01
    - http://127.0.0.1:8000/api/weather/stats?station_id=USC00110072
    - http://127.0.0.1:8000/api/weather/stats?date=2014-01-01&station_id=USC00110072
``` 

## Testing

Django's in-built test library is utilized to perform the test on the response of all of the exposed APIs and also checks max temperature is always greater than min temperature on Analytics table.

## CI pipeline

A simple Continuous Integration (CI) workflow is integrated in Github Actions so that **linting** and **testing** are performed on every `push` and `pull requests` to the master branch.
