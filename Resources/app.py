import pandas as pd
import numpy as np


# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import func

import datetime as dt

from sqlalchemy import Column, Integer, String, Float, DateTime

import pymysql
pymysql.install_as_MySQLdb()

from flask import Flask, jsonify



# Database Setup
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)


# Save references to the invoices and invoice_items tables
Measurement = Base.classes.hawaii_meas
Stations = Base.classes.hawaii_stations


# Create our session (link) from Python to the DB
session = Session(engine)

# Flask Setup
app = Flask(__name__)


#Query for the dates and temperature observations from the last year.
#Convert the query results to a Dictionary using date as the key and tobs as the value.
#Return the json representation of your dictionary.


@app.route("/api/v1.0/precipitation")
def last_year():
    one_year_ago = dt.date.today() - dt.timedelta(days=365)
    
    tobs_values = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date < one_year_ago).all()
    
    tobs_totals = []
    
    for value in tobs_values:
        value_dict = {}
        value_dict['date'] = value[0]
        value_dict['tobs'] = float(value[1])
        tobs_totals.append(value_dict)
        
    return jsonify(tobs_totals)
    
    
#/api/v1.0/stations
#Return a json list of stations from the dataset.

@app.route("/api/v1.0/stations")
def stations():
    stations = stations.query(Stations.name).all()
    
    stations_list = list(np.ravel(stations))

    return jsonify(stations_list)


#/api/v1.0/tobs

#Return a json list of Temperature Observations (tobs) for the previous year

@app.route("/api/v1.0/tobs")
def prev_tobs():
    start_date = '2017-01-01'
    end_date = '2017-12-31'
    
    ly = session.query(Measurement.name, Measurement.date, Measurement.tobs).\
    filter(Measurement.date >= start_date, Measurement.date <= end_date).all()
    
    ly_summary = []
    
    for value in ly:
        value_dict = {}
        value_dict['name'] = value.name
        value_dict['date'] = value.date
        value_dict['tobs'] = value.tobs
        ly_summary.append(value_dict)
        
    return jsonify(ly_summary)
    

#/api/v1.0/<start> and /api/v1.0/<start>/<end>

#Return a json list of the minimum temperature, the average temperature, and the max temperature 
#for a given start or start-end range.

#When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.

#When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start 
#and end date inclusive.


start_date = input('What start date would you like to use? YYYY-MM-DD ')
end_date = input('What end date would you like to use? YYYY-MM-DD ')

@app.route('/api/v1.0/<' + start_date + '>')
@app.route('/api/v1.0/<' + start_date + '>/<' + end_date +'>')



if((start_date is not None) and (end_date is None)):
    def start_date(start_date):
        min_temp = session.query(Measurement.station, func.min(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()
    
        max_temp = session.query(Measurement.station, func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()
    
        avg_temp = session.query(Measurement.station, func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()
    
        values = []
    
        for value in values:
            row = {}
            row['min'] = value.min_temp
            row['max'] = value.max_temp
            row['avg'] = value.avg_temp
            values.append(row)
        
        return jsonify(values)
    
elif((start_date is not None) and (end_date is not None)):

    def start_end(start_date, end_date=None):
        min_temp = session.query(Measurement.station, func.min(Measurement.tobs)).\
        filter(Measurement.date >= start_date, Measurement.date >= end_date).all()
    
        max_temp = session.query(Measurement.station, func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date, Measurement.date >= end_date).all()
    
        avg_temp = session.query(Measurement.station, func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start_date, Measurement.date >= end_date).all()
    
        values = []
    
        for value in values:
            row = {}
            row['min'] = value.min_temp
            row['max'] = value.max_temp
            row['avg'] = value.avg_temp
            values.append(row)
        
        return jsonify(values)

    

else:
    print('You need at lease a start date.')
