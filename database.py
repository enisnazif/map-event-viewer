from sqlalchemy import create_engine, MetaData, Integer, Text, Float, Date, TIMESTAMP, Table, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
import pandas as pd
import glob
import os

#Setup
user = 'Enis'
password = ""
db = 'divvy'
host = 'localhost'
port = 5432

url = 'postgresql+psycopg2://{}:{}@{}:{}/{}'
url = url.format(user, password, host, port, db)
engine = create_engine(url, client_encoding='utf8')

db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

#Loads the trips data into the table
def populate_divvy_trips():
    path = './Data/Divvy/Trips/'
    all_files = glob.glob(os.path.join(path, "*.csv"))
    engine_rc = engine.raw_connection()
    cursor = engine_rc.cursor()

    for filepath in all_files:
        f = open(filepath)
        command = "COPY trips FROM STDIN WITH DELIMITER ',' CSV HEADER"
        cursor.copy_expert(command, f)
        engine_rc.commit()
        print "Loaded " + str(filepath) + " !"

#Loads the stations data into the table
def populate_divvy_stations():
    path = './Data/Divvy/Stations/'
    all_files = glob.glob(os.path.join(path, "*.csv"))
    engine_rc = engine.raw_connection()
    cursor = engine_rc.cursor()

    for filepath in all_files:
        f = open(filepath)
        command = "COPY stations FROM STDIN WITH DELIMITER ',' CSV HEADER"
        cursor.copy_expert(command, f)
        engine_rc.commit()
        print "Loaded " + str(filepath) + " !"

#Populates the created tables with the values from the CSV files
def populate_divvy():
    populate_divvy_stations()
    populate_divvy_trips()

#Gets the names and coordinates of stations in the stations table
def get_divvy_stations():
    engine_rc = engine.raw_connection()
    cursor = engine_rc.cursor()
    cursor.execute("SELECT name,latitude,longitude FROM stations")
    records = cursor.fetchall()
    return records

def init_db():
    from models import Stations, Trips
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    populate_divvy()

################################################################################
