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
    cursor.execute("SELECT area_numbe, community, ST_AsGeoJson(geom) FROM districts;")
    result = cursor.fetchall()
    return result

def get_chicago_neighborhoods():
    cursor.execute("SELECT gid, pri_neigh, ST_AsGeoJson(geom) FROM neighborhoods;")
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

def get_trips_beginning_and_ending_between_times(start_time, end_time):
    cursor.execute("SELECT * FROM TRIPS WHERE start_time = '" + start_time + "'::timestamp AND stop_time = '" + end_time + "'::timestamp;")
    result = cursor.fetchall()
    return result
