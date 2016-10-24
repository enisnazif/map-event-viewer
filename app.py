from flask import Flask, render_template
from database import db_session, init_db
from queries import get_divvy_stations, join_stations_and_trips, get_chicago_districts, add_station_geom
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

@app.route("/")
def showMap():
    return render_template('map.html', stations=stations, joined_tables=joined_tables, districts=districts)

if __name__ == "__main__":
    init_db();
    add_station_geom();
    stations = get_divvy_stations()
    joined_tables = join_stations_and_trips()
    districts = get_chicago_districts()
    app.run()
