from sqlalchemy import Integer, Text, Float, Date, TIMESTAMP, Table, Column
from database import Base

class Stations(Base):
    __tablename__ = 'stations'

    id = Column(Integer, primary_key=True)
    name = Column(Text)
    latitude = Column(Float)
    longitude = Column(Float)
    dpcapacity = Column(Integer)
    online_date = Column(Date)

class Trips(Base):
    __tablename__ = 'trips'

    trip_id = Column(Integer, primary_key=True) #Work out why I can't set this as PK
    starttime = Column(TIMESTAMP)
    stoptime = Column(TIMESTAMP)
    bikeid = Column(Integer)
    tripduration = Column(Integer)
    from_station_id = Column(Integer)
    from_station_name = Column(Text)
    to_station_id = Column(Integer)
    to_station_name = Column(Text)
    usertype = Column(Text)
    gender = Column(Text)
    birthday = Column(Integer)