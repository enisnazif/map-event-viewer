from database import db_session, engine

engine_rc = engine.raw_connection()
cursor = engine_rc.cursor()

#Gets the names and coordinates of stations in the stations table
def get_divvy_stations():
    cursor.execute("SELECT name, latitude, longitude FROM stations")
    result = cursor.fetchall()
    return result

def join_stations_and_trips():
    cursor.execute("")
    result = cursor.fetchall()
    return result

def get_trips_originating_at(station_id):
    cursor.execute("SELECT * FROM TRIPS WHERE from_station_id = " + station_id )
    result = cursor.fetchall()
    return result

def get_trips_terminating_at(station_id):
    cursor.execute("SELECT * FROM TRIPS WHERE to_station_id = " + station_id )
    result = cursor.fetchall()
    return result
