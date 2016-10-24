from database import db_session, engine

#create the raw_connection and engine for SQL statements
engine_rc = engine.raw_connection()
cursor = engine_rc.cursor()

#adds the geom column to stations
def add_station_geom():
    cursor.execute("ALTER TABLE stations ADD COLUMN geom geometry(POINT,4326);")
    cursor.execute("UPDATE stations SET geom = ST_SetSRID(ST_MakePoint(longitude,latitude),4326);")
    
#Gets the names and coordinates of all stations in the stations table
def get_divvy_stations():
    cursor.execute("SELECT name, ST_AsGeoJson(geom) FROM stations")
    result = cursor.fetchall()
    return result

def get_chicago_districts():
    cursor.execute("SELECT area_numbe, community, ST_AsGeoJson(geom) FROM DISTRICTS;")
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
