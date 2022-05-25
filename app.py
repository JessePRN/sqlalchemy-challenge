import numpy as np

import sqlalchemy
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
measurementTable = Base.classes.measurement
stationTable = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    start = "<start>"
    end = "<end>"
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;<br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Query all passengersb

    lastYearPrecip = session.query(measurementTable.date, measurementTable.prcp).\
        filter(measurementTable.date >= '2016-08-23').all()
    

    session.close()

    # Convert list of tuples into normal list
    lastYearPrecipList = []

    for date, prcp in lastYearPrecip:
            precipRow = {}
            precipRow["date"] = date
            precipRow["prcp"] = prcp
            lastYearPrecipList.append(precipRow)
    
    return jsonify(lastYearPrecipList)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of passenger data including the name, age, and sex of each passenger"""
    # Query stations
    
    mostActiveStations = session.query(measurementTable.station, func.count(measurementTable.station)).\
            group_by(measurementTable.station).\
            order_by(func.count(measurementTable.station).desc()).all()
    
    lastYearMostAciveTobsClean = []
    for each in mostActiveStations:
        lastYearMostAciveTobsClean.append(each[0])
          
    
    session.close()

    return jsonify(lastYearMostAciveTobsClean)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of passenger data including the name, age, and sex of each passenger"""
    # Query stations
    
    lastYearMostAciveTobs = session.query(measurementTable.tobs).\
                                filter(measurementTable.station=='USC00519281').\
                                filter(measurementTable.date >= '2016-08-23').\
                                order_by(measurementTable.date.desc()).all()
    lastYearMostAciveTobsClean = []
    for each in lastYearMostAciveTobs:
        lastYearMostAciveTobsClean.append(each[0])
    
    session.close()

    return jsonify(lastYearMostAciveTobsClean)   


@app.route("/api/v1.0/<start>")
def tempSince(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of passenger data including the name, age, and sex of each passenger"""
    # Query stations
    
    tmp = [func.min(measurementTable.tobs),
       func.max(measurementTable.tobs),
       func.avg(measurementTable.tobs)]
                
    tempSince = session.query(*tmp).filter(measurementTable.station=='USC00519281').\
        filter(measurementTable.date >= start).all()
    
    session.close()

    returnList = []
    for each in tempSince[0]:
        returnList.append(each)

    return jsonify(returnList)

@app.route("/api/v1.0/<start>/<end>")
def tempBetween(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of passenger data including the name, age, and sex of each passenger"""
    # Query stations
    
    tmp = [func.min(measurementTable.tobs),
       func.max(measurementTable.tobs),
       func.avg(measurementTable.tobs)]
                
    tempSince = session.query(*tmp).filter(measurementTable.station=='USC00519281').\
        filter(measurementTable.date >= start).\
        filter(measurementTable.date <= end).all()
    
    session.close()

    returnList = []
    for each in tempSince[0]:
        returnList.append(each)

    return jsonify(returnList)

# /api/v1.0/tobs
# Query the dates and temperature observations of the most active station for the previous year of data.
# Return a JSON list of temperature observations (TOBS) for the previous year.

# /api/v1.0/<start> and /api/v1.0/<start>/<end>
# Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a given start or start-end range.
# When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than or equal to the start date.
# When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates from the start date through the end date (inclusive).


if __name__ == '__main__':
    app.run(debug=True)
