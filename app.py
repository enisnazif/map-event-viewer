from flask import Flask, render_template
from database import db_session, init_db
from queries import get_divvy_stations

app = Flask(__name__)

@app.route('/')
def showLanding():
    return render_template('index.html')

@app.route("/map")
def showMap():
    return render_template('map.html', stations=stations)

@app.route("/events")
def showEvents():
    return render_template('events.html')

if __name__ == "__main__":
    init_db();
    stations = get_divvy_stations()
    app.run(debug=True)
