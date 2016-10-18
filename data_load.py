import psycopg2

def get_stations(user):
    try:
        conn = psycopg2.connect("host='localhost' dbname='divvy' user='"+user+"'")
    except:
        print "Unable to connect"
    cursor = conn.cursor()
    cursor.execute("SELECT name,latitude,longitude FROM STATIONS")
    records = cursor.fetchall()
    return records
