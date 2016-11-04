###############################################################################
# Phase 1: A simple point anomaly detection system applied to each timeseries of
# arrival and departure counts (not taking into account the spatial dimension)
# Maybe use an ARIMA model to capture seasonality
#
# Phase 2: Incorporate spatial dimension somehow
#
###############################################################################
import divvy_queries as dq
#import matplotlib.pyplot as plt
import pandas as pd

#Computes the ward arrival time
def get_ward_timeseries(wards_list,minute_bin):
    ward_arrivals_timeseries = []
    ward_departures_timeseries = []

    #For each ward, get the arrivals and departures timeseries
    for i in wards_list:
        print 'Getting arrivals timeseries for ward ' + str(i)
        ward_arrivals_timeseries.insert(i,dq.get_timeseries_of_trips_arriving_in_ward(str(i), str(minute_bin)))
        print 'Getting departures timeseries for ward ' + str(i)
        ward_departures_timeseries.insert(i,dq.get_timeseries_of_trips_departing_from_ward(str(i), str(minute_bin)))

    return {'arrivals': ward_arrivals_timeseries, 'departures': ward_departures_timeseries}


#Get the arrival and departure timeseries by ward, binned by 30 minute intervals
#timeseries = get_ward_timeseries([9,3,42],30)
