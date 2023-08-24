# Import the dependencies.
import warnings
warnings.filterwarnings('ignore')
from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import func
import numpy as np
#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")


# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine) 

Base.classes.keys()
 # Save references to each table
measure = Base.classes.measurement
stations = Base.classes.station
# Create our session (link) from Python to the DB
session = Session(engine)

# Define a basic route to check if the app is running

# # Create our session (link) from Python to the DB
session = Session(engine)

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
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<end>"
    )


@app.route("/api/v1.0/precipitation")
def months():
    session = Session(engine)
    info = session.query(measure.tobs,measure.prcp).filter(measure.station == 'USC00519281').filter(measure.date >= '2016-08-18').all()
    session.close()

    month_info = []
    for tobs,prcp in info:
        month_dict = {}
        month_dict["tobs"] = tobs
        month_dict["prcp"] = prcp
        month_info.append(month_dict)

    return jsonify(month_info)


@app.route("/api/v1.0/stations")
def all_stations():
    session = Session(engine)
    results = session.query(measure.station.distinct()).all()
    session.close()

    stations = list(np.ravel(results))

    return jsonify(stations)


@app.route("/api/v1.0/tobs")
def tobs():
    
    session = Session(engine)

    results_date = session.query(measure.date, measure.tobs).filter(measure.station == 'USC00519281').filter(measure.date >= '2016-08-18').all()

    session.close()
    
    return jsonify(results_date)

@app.route("/api/v1.0/<start>")
def start():
    
    session = Session(engine)

    results_date = session.query(measure.date, measure.tobs).filter(measure.station == 'USC00519281').filter(measure.date >= '2016-08-18').all()

    session.close()

    month_info = []
    for tobs in results_date:
        month_info.append(measure.tobs)

    
    return jsonify(results_date)

@app.route("/api/v1.0/<end>")
def end():
    
    session = Session(engine)

    results_date = session.query(measure.date, measure.tobs).filter(measure.station == 'USC00519281').filter(measure.date <= '2016-08-18').all()

    session.close()

    month_info_end = []
    for tobs in results_date:
        month_info_end.append(measure.tobs)

    return jsonify(results_date)

if __name__ == "__main__":
    app.run(debug=True)
