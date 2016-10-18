from flask import Flask, render_template
from data_load import get_stations
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)

@app.route('/')
def showLanding():
    return render_template('index.html')

@app.route("/map")
def showMap():
    stations = get_stations('Enis');
    return render_template('map.html', stations=stations)

@app.route("/events")
def showEvents():
    return render_template('events.html')

if __name__ == "__main__":
    app.run(debug=True)
