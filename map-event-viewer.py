from flask import Flask, render_template, request, redirect
import divvy_queries as dq
import divvy_event_detection as ded
import ny_queries as nyq
from flask_socketio import SocketIO, send, emit
from random import randint

#Initalise application
app = Flask(__name__)
socketio = SocketIO(app)

#Landing page
@app.route("/")
def show_landing_page():
    return 'Select a dataset: <br> <a href="/divvy">Divvy Chicago Bikeshare</a> <br> <a href="/ny">New York Taxi</a>'

#Divvy page
@app.route("/divvy")
def show_divvy_map():
    #render the template with the default values
    return render_template('divvy_map.html',
        stations = dq.get_divvy_stations_json(),
        regions = dq.get_chicago_precincts_json(),
        events = 'No events',
        detection_method = 'Method A',
        show_stations = 'True',
        show_trips = 'True',
        show_events = 'True',
        start_date_time = '2016-01-01 12:00',
        end_date_time = '2016-01-01 13:00'
    )

#NY taxi page
@app.route("/ny")
def show_ny_map():
    #render the template with the default values
    return render_template('ny_map.html',
        events = 'No events',
        regions = nyq.get_ny_taxi_zones(),
        detection_method = 'Method A',
        show_trips = 'True',
        show_events = 'True',
        end_date_time = '12-31-2016 00:00',
        start_date_time = '01-01-2013 00:00'
    )


################################################################################
# Divvy socket event handlers
################################################################################

#Handles the change in the datetime range for Divvy
@socketio.on('datetime_range_updated', namespace='/divvy')
def handle_datetime_update(message):
    trips_beginning_between_times = dq.get_trips_beginning_between_times(message.values()[1], message.values()[0]).to_json()
    emit('trips_updated', trips_beginning_between_times, namespace='/divvy')
    emit('events_updated', '', namespace='/divvy')

#Handles the change in the detection method for Divvy
@socketio.on('detection_method_updated', namespace='/divvy')
def handle_settings_updated(message):
    print 'Divvy detection method update' + str(message)
    #Get the new events here
    emit('events_updated', '', namespace='/divvy')

################################################################################
# NY socket event handlers
################################################################################

#Handles the change in the datetime range for NY
@socketio.on('datetime_range_updated', namespace='/ny')
def handle_datetime_update(message):
    print 'NY datetime update'
    #Get the new events here
    emit('events_updated',str(randint(0,9)), namespace='/ny')

#Handles the change in the detection method for NY
@socketio.on('detection_method_updated', namespace='/ny')
def handle_detection_method_update(message):
    print 'NY detection method update'
    #Get the new events here
    emit('events_updated',str(randint(0,9)), namespace='/ny')
