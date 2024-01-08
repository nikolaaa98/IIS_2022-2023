import datetime
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer, Float, DateTime,Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import enum

db = create_engine('sqlite:///C:/Users/User/Desktop/InteligentniSiste/IIS_2022-2023/weather.db', echo=True)

base = declarative_base()

Session = sessionmaker(db)
session = Session()

class WeatherType(enum.Enum):
    Rain = 0
    Rain_Overcast = 0.12
    Rain_Partially_cloudy = 0.24
    Partially_cloudy = 0.36
    Clear = 0.48
    Snow = 0.6
    Snow_Partially_cloudy = 0.72
    Snow_Overcast = 0.84
    Overcast = 0.96
    
class Weather(base):
    
    __tablename__ = 'weather_test'

    id = Column(Integer, primary_key=True)
    time_stamp = Column(DateTime)
    temperature = Column(Float)
    last_hour_temperature = Column(Float)
    yesterday_temperature = Column(Float)

    feels_like = Column(Float)
    humidity = Column(Float)
    wind_gust = Column(Float)
    wind_speed = Column(Float)

    sea_level_pressure = Column(Float)
    cloud_cover = Column(Float)
    visibility = Column(Float)
    condition = Column(Float)
    day_part = Column(Float)
    day = Column(Integer)
    corona = Column(Integer)
    day_week = Column(Integer)
    temp_day = Column(Integer)

    sin_time = Column(Float)
    cos_time = Column(Float)
    day_sin = Column(Float)
    day_cos = Column(Float)
    sin_month = Column(Float)
    cos_month = Column(Float)

    last_hour_load = Column(Float)
    load = Column(Float)
    
    def __init__(self, **kwargs):
        self.time_stamp = datetime.datetime.strptime(str(kwargs['Time Stamp']), '%Y-%m-%d %H:%M:%S')
        self.temperature = round(float(kwargs['temp']), 2)
        self.last_hour_temperature = round(float(kwargs['last_hour_temperature']), 2)
        self.yesterday_temperature = round(float(kwargs['yesterday_temperature']), 2)

        self.feels_like = round(float(kwargs['feelslike']), 2)
        self.humidity = round(float(kwargs['humidity']), 2)
        self.wind_gust = round(float(kwargs['windgust']), 2)
        self.wind_speed = round(float(kwargs['windspeed']), 2)

        self.sea_level_pressure = round(float(kwargs['sealevelpressure']), 2)
        self.cloud_cover = round(float(kwargs['cloudcover']), 2)
        self.visibility = round(float(kwargs['visibility']), 2)
        temp = kwargs['conditions'].replace(' ', '_').replace(',', '')
        self.condition = round(float(WeatherType[temp].value), 2)
        self.day_part = round(float(kwargs['day_part']), 2)
        self.day = int(kwargs['day'])
        self.corona = int(kwargs['corona'])
        self.day_week = int(kwargs['day_week'])
        self.temp_day = int(kwargs['temp_day'])

        self.sin_time = round(float(kwargs['sin_time']), 2)
        self.cos_time = round(float(kwargs['cos_time']), 2)
        self.day_sin = round(float(kwargs['cos_time']), 3)
        self.day_cos = round(float(kwargs['cos_time']) ,3)
        self.sin_month = round(float(kwargs['sin_month']), 3)
        self.cos_month = round(float(kwargs['cos_month']), 3)

        self.last_hour_load = round(float(kwargs['last_hour_load']), 2)
        self.load = round(float(kwargs['Load']), 2)

def impute(df, col_name):
    import numpy as np
    for ind in df.index:
        if np.isnan(df[col_name][ind]):
            temp = df[col_name].iloc[ind - 15:ind + 15].dropna()
            df[col_name][ind] = temp.mean()

def return_all_elements():

    res = pd.read_sql_table('weather',db).drop(['id','time_stamp'], axis=1)

    impute(res,'wind_gust')
    impute(res,'load')
    impute(res,'humidity')
    return res

def return_elements_from_database_in_range(start_date,end_date):
    res = pd.read_sql_table('weather', db)
    impute(res, 'wind_gust')
    impute(res, 'load')

    impute(res, 'humidity')
    res['date'] = pd.to_datetime(res['time_stamp']).dt.date
    res = res[(res['date'] >= start_date) & (res['date'] <= end_date)]
    res = res.drop(['id', 'time_stamp','date'], axis=1)
    return res

def return_elements_from_database_in_range_predict(start_date,end_date):
    res = pd.read_sql_table('weather_test', db)
    impute(res, 'wind_gust')

    impute(res, 'humidity')
    res['date'] = pd.to_datetime(res['time_stamp']).dt.date
    res = res[(res['date'] >= start_date) & (res['date'] <= end_date)]
    res = res.drop(['id', 'time_stamp','date'], axis=1)
    #TODO 2 samo izbrisati jer nacin 1 popuni sa srednjim vrednostima

    return res

def store_to_database(model : Weather):
    #TODO 1 nacin gde trazim datime iste samo bez godine i lepim srednje vrednosti
    last_hour_load, load = correct_data_by_mean(model.time_stamp, model.day_week)
    model.load = load
    model.last_hour_load = last_hour_load

    session.add(model)
    session.commit()

def correct_data_by_mean(start_date, day_week):
    start_date = datetime.datetime.strftime(start_date, '%H:%M:%S')
    res = pd.read_sql_table('weather', db)
    res = res[res['day_week'] == day_week]
    res = res[-72:]
    res['date'] = pd.to_datetime(res['time_stamp']).dt.strftime('%H:%M:%S')

    res = res[(res['date'] == start_date)]
    load = res['load'].mean()

    last_hour_load = res['last_hour_load'].mean()
    
    return round(last_hour_load, 2) , round(load, 2)


if __name__ == "__main__":
    base.metadata.create_all(db)