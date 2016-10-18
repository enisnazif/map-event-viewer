#This module is reponsible for creating the tables that will be used for


from sqlalchemy import create_engine, MetaData, Integer, Text, Float, Date, TIMESTAMP, Table, Column
from sqlalchemy.orm import sessionmaker
import pandas as pd
import glob
import os

#Connects to the database db, with the specified login credentials
def connect(user, password, db, host='localhost', port=5432):
    url = 'postgresql+psycopg2://{}:{}@{}:{}/{}'
    url = url.format(user, password, host, port, db)

    conn = create_engine(url, client_encoding='utf8')
    meta = MetaData(bind=conn, reflect=True)

    return conn, meta

#Creates the tables for the Divvy dataset and returns references to the tables
def create_divvy_tables(conn, meta):
    #Define the stations table
	stations = Table('stations', meta,
        Column('id', Integer, primary_key=True),
        Column('name', Text),
        Column('latitude', Float),
        Column('longitude', Float),
        Column('dpcapacity', Integer),
        Column('online_date', Date)
	)

    #Define the trips table
	trips = Table('trips', meta,
        Column('trip_id', Integer, primary_key=True),
        Column('starttime', TIMESTAMP),
        Column('stoptime', TIMESTAMP),
        Column('bikeid', Integer),
        Column('tripduration', Integer),
        Column('from_station_id', Integer),
        Column('from_station_name', Text),
        Column('to_station_id', Integer),
        Column('to_station_name', Text),
        Column('usertype', Text),
        Column('gender', Text),
        Column('birthday', Integer)
	)
        meta.create_all(conn)
        return stations, trips

#Loads the trips data into the table
def populate_divvy_trips(conn):
    path = './Data/Divvy/Trips/'
    all_files = glob.glob(os.path.join(path, "*.csv"))
    conn = conn.raw_connection()
    cursor = conn.cursor()

    for filepath in all_files:
        f = open(filepath)
        command = "COPY trips FROM STDIN WITH DELIMITER ',' CSV HEADER"
        cursor.copy_expert(command, f)
        conn.commit()
        print "Loaded " + str(filepath) + " !"

#Loads the stations data into the table
def populate_divvy_stations(conn):
    path = './Data/Divvy/Stations/'
    all_files = glob.glob(os.path.join(path, "*.csv"))
    conn = conn.raw_connection()
    cursor = conn.cursor()

    for filepath in all_files:
        f = open(filepath)
        command = "COPY stations FROM STDIN WITH DELIMITER ',' CSV HEADER"
        cursor.copy_expert(command, f)
        conn.commit()
        print "Loaded " + str(filepath) + " !"

#Populates the created tables with the values from the CSV files
def populate_divvy(conn):
    populate_divvy_stations(conn)
    populate_divvy_trips(conn)

def execute_query(conn):
    session = sessionmaker(bind=conn)

def init_divvy():
    conn, meta = connect('Enis', "", 'divvy')
    create_divvy_tables(conn, meta)
    populate_divvy(conn)


init_divvy()
