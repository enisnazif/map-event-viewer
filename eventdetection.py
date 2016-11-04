# DUMMY MODULE #
import pandas as pd
import divvy_queries as dq

################################################################################
# General event class:
#
# A detected event will have the following attributes:
#
# id: A unique identification number for the event
#
# start_time: A timestamp detailing when the event began
#
# end_time: A timestamp detailing when the event ended
#
# affected_location: An array of points that specify the polygon, representing
# the area over which the event occured
#
# details: A string that may or may not contain some specific details about the
# event, accuired from various news sources?
################################################################################

class Event:
    id = None
    start_time = None
    end_time = None
    affected_location = None
    details = None

    def __init__(self, id, start_time, end_time, affected_location, details):
        self.id = id
        self.start_time = start_time
        self.end_time = end_time
        self.affected_location = affected_location
        self.details = details

    def serialise(self):
        return {
            'id': self.id,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'affected_location': self.affected_location,
            'details': self.details
        }

def get_data():
    data = dq.join_stations_and_trips()

#This function returns the detected events
def get_events():
    e1 = Event(1,"12/12/2016 11:43:01","13/12/2016 11:43:01",[[83.01,-72,12],[84.01,-71,12],[85.01,-73,12]], 'Something happened :o')
    e2 = Event(2,"12/12/2016 11:43:01","13/12/2016 11:43:01",[[83.01,-72,12],[84.01,-71,12],[85.01,-73,12]], 'Something happened :o')
    e3 = Event(3,"12/12/2016 11:43:01","13/12/2016 11:43:01",[[83.01,-72,12],[84.01,-71,12],[85.01,-73,12]], 'Something happened :o')
    e4 = Event(4,"12/12/2016 11:43:01","13/12/2016 11:43:01",[[83.01,-72,12],[84.01,-71,12],[85.01,-73,12]], 'Something happened :o')

    events = [e1,e2,e3,e4]

    return events

def detect_events(data):
    print 'got to detect events'
    data = pd.DataFrame(data)
    print data
