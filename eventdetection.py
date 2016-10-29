import pandas as pd

class Event:

    name = ''
    location = [0,0]


    def __init__(self, name, location):
        self.name = name
        self.location = location

def detect_events(data):
    events = [Event('Stabbing', [12,42]), Event('Free Cake',[12,19])]
    return events
