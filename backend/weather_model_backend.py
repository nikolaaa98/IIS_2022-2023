import datetime
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer, Float, DateTime,Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import enum

db_string = 'sqlite:///C:/Users/User/Desktop/InteligentniSiste/IIS_2022-2023/weather.db'

db = create_engine(db_string)
base = declarative_base()

Session = sessionmaker(db)
session = Session()
