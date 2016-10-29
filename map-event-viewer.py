from flask import Flask, render_template, request, redirect
import divvy_queries
from eventdetection import detect_events
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

stations = divvy_queries.get_divvy_stations()
districts = divvy_queries.get_chicago_districts()
events =
#declare all template variables and set to null
dataset = None
detection_method = None
show_stations = None
show_trips = None
show_events = None
end_date_time = None
start_date_time = None

@app.route("/")
def show_map():
    #set default values for template variables
    dataset = 'Divvy'
    detection_method = 'Method A'
    show_stations = 'True'
    show_trips = 'True'
    show_events = 'True'
    end_date_time = '01-01-2013 00:00:00'
    start_date_time = '12-31-2016 00:00:00'
    return render_template('map.html', stations=stations, districts=districts, dataset=dataset, detection_method=detection_method, events=events)

@socketio.on('settings_updated')
def handle_settings_updated(message):
    dataset = message.values()[1]
    detection_method = message.values()[0]

    #Do something with dataset and detection_method below...
    print dataset
    print detection_method

@socketio.on('parameters_updated')
def handle_settings_updated(message):
    show_stations = message.values()[0]
    show_trips = message.values()[1]
    show_events = message.values()[4]
    end_date_time = message.values()[2]
    start_date_time = message.values()[3]

    if(end_date_time != '' and start_date_time != ''):
        data_matching_criteria = get_trips_beginning_between_times(start_date_time, end_date_time)
        detected_events = detect_events(data_matching_criteria)

        print 'done'

    #Do something with all of these values below...
    #might be good to implement some kind of way of checking for changes s
