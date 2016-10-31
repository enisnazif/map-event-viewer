import psycopg2

try:
    conn = psycopg2.connect("dbname='divvy' user=Enis host='localhost' password=''")
except:
    print "I am unable to connect to the database"

cursor = conn.cursor()

#Gets the names and coordinates of all stations in the stations table
def get_divvy_stations():
    cursor.execute("SELECT name, ST_AsGeoJson(geom) FROM stations")
    result = cursor.fetchall()
    return result

#Returns in geoJSON format a list of points describing each district of Chicago
def get_chicago_districts():
    cursor.execute("SELECT community, ST_AsGeoJson(geom) FROM districts;")
    result = cursor.fetchall()
    return result

def get_chicago_precincts():
    cursor.execute("SELECT full_text, ST_AsGeoJson(geom) FROM precincts;")
    result = cursor.fetchall()
    return result

#Returns (trip_id, starttime, stoptime, start_latitude, start_longitude, stop_latitude, stop_longitude) tuples
def join_stations_and_trips():
    cursor.execute(
        "SELECT trips.trip_id, trips.starttime, trips.stoptime, s1.latitude, s1.longitude, s2.latitude, s2.longitude " +
        "FROM trips, stations s1, stations s2 " +
        "WHERE s1.id = trips.from_station_id AND s2.id = trips.to_station_id;")
    result = cursor.fetchall()
    return result

#Gets all the trips originating at the station with id 'station_id'
def get_trips_originating_at(station_id):
    cursor.execute("SELECT * FROM TRIPS WHERE from_station_id = " + station_id )
    result = cursor.fetchall()
    return result

#Gets all the trips terminating at the station with id 'station_id'
def get_trips_terminating_at(station_id):
    cursor.execute("SELECT * FROM TRIPS WHERE to_station_id = " + station_id )
    result = cursor.fetchall()
    return result

#Gets all the trips with a starttime between start_time and end_time
def get_trips_beginning_between_times(start_time, end_time):
    cursor.execute("SELECT * FROM TRIPS WHERE starttime BETWEEN '" + start_time + "'::timestamp AND '" + end_time + "'::timestamp;")
    result = cursor.fetchall()
    return result

#Gets all the trips with a stoptime between start_time and end_time
def get_trips_ending_between_times(start_time, end_time):
    cursor.execute("SELECT * FROM TRIPS WHERE stoptime BETWEEN '" + start_time + "'::timestamp AND '" + end_time + "'::timestamp;")
    result = cursor.fetchall()
    return result

#Gets all the trips which take place between start_time and end_time
def get_trips_beginning_and_ending_between_times(start_time, end_time):
    cursor.execute("SELECT * FROM TRIPS WHERE start_time = '" + start_time + "'::timestamp AND stop_time = '" + end_time + "'::timestamp;")
    result = cursor.fetchall()
    return result

#Get all the stations in a district
def get_stations_in_district(district):
    cursor.execute("SELECT s.name, d.community FROM DISTRICTS d, STATIONS s WHERE d.geom && s.geom AND ST_Contains(d.geom, s.geom);")
    result = cursor.fetchall()
    return result

#Get all the stations in a precinct
def get_stations_in_precinct(precinct):
    cursor.execute("SELECT s.name FROM PRECINCTS p, STATIONS s WHERE p.geom && s.geom AND ST_Contains(p.geom, s.geom) AND p.precinct="+precinct_number+");")
    result = cursor.fetchall()
    return result

def get_trips_originating_in_district(district):
    cursor.execute("SELECT * FROM TRIPS t WHERE t.from_station_name IN (SELECT s.name FROM DISTRICTS d, STATIONS s WHERE d.geom && s.geom AND ST_Contains(d.geom, s.geom) AND d.area_numbe='"+district+"');")
    result = cursor.fetchall()
    return result

def get_trips_originating_in_precinct(precinct):
    cursor.execute("SELECT * FROM TRIPS t WHERE t.from_station_name IN (SELECT s.name FROM PRECINCTS p, STATIONS s WHERE p.geom && s.geom AND ST_Contains(p.geom, s.geom) AND p.precinct="+precinct+");")
    result = cursor.fetchall()
    return result

def get_trips_terminating_in_district(district):
    cursor.execute("SELECT * FROM TRIPS t WHERE t.to_station_name IN (SELECT s.name FROM DISTRICTS d, STATIONS s WHERE d.geom && s.geom AND ST_Contains(d.geom, s.geom) AND d.area_numbe='"+district+"');")
    result = cursor.fetchall()
    return result

def get_trips_terminating_in_precinct(precinct):
    cursor.execute("SELECT * FROM TRIPS t WHERE t.to_station_name IN (SELECT s.name FROM PRECINCTS p, STATIONS s WHERE p.geom && s.geom AND ST_Contains(p.geom, s.geom) AND p.precinct="+precinct+");")
    result = cursor.fetchall()
    return result

def get_trips_going_between_districts(start_district, end_district):
    cursor.execute("SELECT * FROM TRIPS t WHERE t.from_station_name IN (SELECT s.name FROM DISTRICTS d, STATIONS s WHERE d.geom && s.geom AND ST_Contains(d.geom, s.geom) AND d.area_numbe='"+start_district+"') AND t.to_station_name IN (SELECT s.name FROM DISTRICTS d, STATIONS s WHERE d.geom && s.geom AND ST_Contains(d.geom, s.geom) AND d.area_numbe='"+end_district+"');")
    result = cursor.fetchall()
    return result

def get_trips_going_between_precincts(start_precinct, end_precinct):
    cursor.execute("SELECT * FROM TRIPS t WHERE t.from_station_name IN (SELECT s.name FROM PRECINCTS p, STATIONS s WHERE p.geom && s.geom AND ST_Contains(p.geom, s.geom) AND p.precinct="+start_precinct+") AND t.to_station_name IN (SELECT s.name FROM PRECINCTS p, STATIONS s WHERE p.geom && s.geom AND ST_Contains(p.geom, s.geom) AND p.precinct="+end_precinct+");")
    result = cursor.fetchall()
    return result
