import psycopg2

try:
    conn = psycopg2.connect("dbname='ny_taxi' user=Enis host='localhost' password=''")
except:
    print "Unable to connect to the database"

cursor = conn.cursor()

#Returns in geoJSON format a list of points describing each district of New York
def get_ny_communities():
    query = "SELECT borocd, ST_AsGeoJson(ST_Transform(geom,4326)) FROM communities;"
    cursor.execute(query)
    result = cursor.fetchall()
    return result

#Returns in geoJSON format a list of points describing each taxi zone of New York
def get_ny_taxi_zones():
    query = "SELECT zone, ST_AsGeoJson(ST_Transform(geom,4326)) FROM taxi_zones;"
    cursor.execute(query)
    result = cursor.fetchall()
    return result
