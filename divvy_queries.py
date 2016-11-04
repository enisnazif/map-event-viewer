import psycopg2
import pandas as pd

try:
    conn = psycopg2.connect("dbname='divvy' user=Enis host='localhost' password=''")
except:
    print "Unable to connect to the database"

cursor = conn.cursor()

#Gets the names and coordinates of all stations in the stations table
def get_divvy_stations_json():
    query = "SELECT name, ST_AsGeoJson(geom) FROM stations"
    cursor.execute(query)
    result = cursor.fetchall()
    return result

#Returns in geoJSON format a list of points describing each district of Chicago
def get_chicago_districts_json():
    query = "SELECT community, ST_AsGeoJson(geom) FROM districts;"
    cursor.execute(query)
    result = cursor.fetchall()
    return result

#Returns in geoJSON format a list of points describing each district of Chicago
def get_chicago_precincts_json():
    query = "SELECT full_text, ST_AsGeoJson(geom) FROM precincts;"
    cursor.execute(query)
    result = cursor.fetchall()
    return result

def get_chicago_precinct_list():
    query = "SELECT DISTINCT precinct AS precinct_number FROM precincts"
    result = pd.read_sql_query(query,conn)
    return result

#Returns (trip_id, starttime, stoptime, start_latitude, start_longitude, stop_latitude, stop_longitude) tuples
def join_stations_and_trips():
    query = "SELECT trips.trip_id, trips.starttime, trips.stoptime, s1.latitude, s1.longitude, s2.latitude, s2.longitude FROM trips, stations s1, stations s2 WHERE s1.id = trips.from_station_id AND s2.id = trips.to_station_id;"
    result = pd.read_sql_query(query,conn)
    return result

#Gets all the trips originating at the station with id 'station_id'
def get_trips_originating_at(station_id):
    query = "SELECT * FROM TRIPS WHERE from_station_id = " + station_id + ";"
    result = pd.read_sql_query(query,conn)
    return result

#Gets all the trips terminating at the station with id 'station_id'
def get_trips_terminating_at(station_id):
    query = "SELECT * FROM TRIPS WHERE to_station_id = " + station_id + ";"
    result = pd.read_sql_query(query,conn)
    return result

#Gets all the trips with a starttime between start_time and end_time (Use YYYY-MM-DD HH:MM:SS Format)
def get_trips_beginning_between_times(start_time, end_time):
    query = "SELECT t.*, ST_AsGeoJson(s1.geom) AS start_geom, ST_AsGeoJson(s2.geom) AS end_geom FROM TRIPS t, STATIONS s1, STATIONS s2 WHERE starttime BETWEEN '" + start_time + "'::timestamp AND '" + end_time + "'::timestamp AND s1.id = from_station_id AND s2.id = to_station_id;"
    result = pd.read_sql_query(query,conn)
    return result

#Gets all the trips with a stoptime between start_time and end_time (Use YYYY-MM-DD HH:MM:SS Format)
def get_trips_ending_between_times(start_time, end_time):
    query = "SELECT * FROM TRIPS WHERE stoptime BETWEEN '" + start_time + "'::timestamp AND '" + end_time + "'::timestamp;"
    result = pd.read_sql_query(query,conn)
    return result

#Gets all the trips which take place between start_time and end_time (Use YYYY-MM-DD HH:MM:SS Format)
def get_trips_beginning_and_ending_between_times(start_time, end_time):
    query = "SELECT * FROM TRIPS WHERE start_time = '" + start_time + "'::timestamp AND stop_time = '" + end_time + "'::timestamp;"
    result = pd.read_sql_query(query,conn)
    return result

#Get all the stations in a district
def get_stations_in_district(district):
    query = "SELECT s.name, d.community FROM DISTRICTS d, STATIONS s WHERE d.geom && s.geom AND ST_Contains(d.geom, s.geom);"
    result = pd.read_sql_query(query,conn)
    return result

#Get all the stations in a precinct
def get_stations_in_precinct(precinct):
    query = "SELECT s.name FROM PRECINCTS p, STATIONS s WHERE p.geom && s.geom AND ST_Contains(p.geom, s.geom) AND p.precinct="+precinct+");"
    result = pd.read_sql_query(query,conn)
    return result

def get_trips_originating_in_district(district):
    query = "SELECT * FROM TRIPS t WHERE t.from_station_name IN (SELECT s.name FROM DISTRICTS d, STATIONS s WHERE d.geom && s.geom AND ST_Contains(d.geom, s.geom) AND d.area_numbe='"+district+"');"
    result = pd.read_sql_query(query,conn)
    return result

def get_trips_originating_in_precinct(precinct):
    query = "SELECT * FROM TRIPS t WHERE t.from_station_name IN (SELECT s.name FROM PRECINCTS p, STATIONS s WHERE p.geom && s.geom AND ST_Contains(p.geom, s.geom) AND p.precinct="+precinct+");"
    result = pd.read_sql_query(query,conn)
    return result

def get_trips_terminating_in_district(district):
    query = "SELECT * FROM TRIPS t WHERE t.to_station_name IN (SELECT s.name FROM DISTRICTS d, STATIONS s WHERE d.geom && s.geom AND ST_Contains(d.geom, s.geom) AND d.area_numbe='"+district+"');"
    result = pd.read_sql_query(query,conn)
    return result

def get_trips_terminating_in_precinct(precinct):
    query = "SELECT * FROM TRIPS t WHERE t.to_station_name IN (SELECT s.name FROM PRECINCTS p, STATIONS s WHERE p.geom && s.geom AND ST_Contains(p.geom, s.geom) AND p.precinct="+precinct+");"
    result = pd.read_sql_query(query,conn)
    return result

def get_trips_going_between_districts(start_district, end_district):
    query = "SELECT * FROM TRIPS t WHERE t.from_station_name IN (SELECT s.name FROM DISTRICTS d, STATIONS s WHERE d.geom && s.geom AND ST_Contains(d.geom, s.geom) AND d.area_numbe='"+start_district+"') AND t.to_station_name IN (SELECT s.name FROM DISTRICTS d, STATIONS s WHERE d.geom && s.geom AND ST_Contains(d.geom, s.geom) AND d.area_numbe='"+end_district+"');"
    result = pd.read_sql_query(query,conn)
    return result

def get_trips_arriving_in_precinct_in_time_range(precinct, start_time, end_time):
    query = "SELECT * FROM TRIPS t WHERE t.to_station_name IN (SELECT s.name FROM PRECINCTS p, STATIONS s WHERE p.geom && s.geom AND ST_Contains(p.geom, s.geom) AND p.precinct="+precinct+") AND stoptime BETWEEN '" + start_time + "'::timestamp AND '" + end_time + "'::timestamp;"
    result = pd.read_sql_query(query,conn)
    return result

#Gets a minute by minute frequency time series of arrivals in precinct
def get_timeseries_of_trips_arriving_in_ward(precinct, minute_bin):
    query = "SELECT date_trunc('hour', stoptime) + date_part('minute', stoptime)::int / "+minute_bin+" * interval '"+minute_bin+" min' AS minute, COUNT(*) FROM TRIPS t WHERE t.from_station_name IN (SELECT s.name FROM PRECINCTS p, STATIONS s WHERE p.geom && s.geom AND ST_Contains(p.geom, s.geom) AND p.ward='"+precinct+"') GROUP BY minute;"
    result = pd.read_sql_query(query,conn)
    return result

#Gets a minute by minute frequency time series of departures in precinct
def get_timeseries_of_trips_departing_from_ward(precinct, minute_bin):
    query = "SELECT date_trunc('hour', starttime) + date_part('minute', starttime)::int / "+minute_bin+" * interval '"+minute_bin+" min' AS minute, COUNT(*) FROM TRIPS t WHERE t.from_station_name IN (SELECT s.name FROM PRECINCTS p, STATIONS s WHERE p.geom && s.geom AND ST_Contains(p.geom, s.geom) AND p.ward='"+precinct+"') GROUP BY minute;"
    result = pd.read_sql_query(query,conn)
    return result
