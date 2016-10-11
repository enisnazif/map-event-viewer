from flask import Flask, render_template
import psycopg2


#Try to connect to the local postgreSQL database 'divvy' as Enis
try:
    conn=psycopg2.connect("host='localhost' dbname='divvy' user='Enis'")
except:
    print "Unable to connect"

#If connection was sucessful, create a cursor, and try a simple query
cursor = conn.cursor()
cursor.execute("SELECT * FROM trips")
records = cursor.fetchall()

print records[1]

app = Flask(__name__)

@app.route('/')
def showLanding():
    return render_template('index.html')

@app.route("/map")
def showMap():
    return render_template('map.html')

@app.route("/events")
def showEvents():
    return render_template('events.html')

if __name__ == "__main__":
    app.run()
