import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func , inspect
from sqlalchemy import distinct
import numpy as np
import datetime as dt

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)
# Save references to each table

measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

# Now that you have completed your initial analysis, design a Flask API based on the queries that you have just developed.

# Use FLASK to create your routes.

app = Flask(__name__)

@app.route("/")
def homepage():
    return (
        f"Vacation Planning Weather API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )
@app.route("/api/v1.0/precipitation")
def precipitation():
#     Convert the query results to a Dictionary using date as the key and prcp as the value.
    session = Session(engine)
    key = measurement.date
    value = measurement.prcp
    results = session.query(key, value).all()

    all_dicts = []
    for date, prcp in results:
        new_dict = {}
        new_dict[date] = prcp
        all_dicts.append(new_dict)

#     Return the JSON representation of your dictionary.
    return jsonify(all_dicts)

@app.route("/api/v1.0/stations")
def stations():
#     Return a JSON list of stations from the dataset.

    session = Session(engine)
    results = session.query(station.name).all()

    json_list = list(np.ravel(results))

    return jsonify(json_list)


@app.route("/api/v1.0/tobs")
def tobs():
#     query for the dates and temperature observations from a year from the last data point.
    year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)
    year_ago = str(year_ago)

    session = Session(engine)
    results = session.query(measurement.date,measurement.tobs)\
        .filter(measurement.date <= '2017-08-23')\
        .filter(measurement.date >= year_ago).all()

    all_dicts = []
    for date, tobs in results:
        new_dict = {}
        new_dict[date] = tobs
        all_dicts.append(new_dict)
#     Return a JSON list of Temperature Observations (tobs) for the previous year.
    return jsonify(all_dicts)


@app.route("/api/v1.0/<start>")
#     Return a JSON list of the minimum temperature, the average temperature,
#     and the max temperature for a given start or start-end range.
def calc_temp(start):
#     """TMIN, TAVG, and TMAX for a list of dates."""
    start = str(start)

    temps = [func.min(measurement.tobs),
            func.max(measurement.tobs),
            func.avg(measurement.tobs)]
#    """Args:
#         start_date (string): A date string in the format %Y-%m-%d
#         end_date (string): A date string in the format %Y-%m-%d
    
#     Returns:
#         TMIN, TAVE, and TMAX
#     """
    session = Session(engine)
    results = session.query(*temps)\
                .filter(measurement.date >= start)\
                .all()

    new_dict = {}
    new_dict["Tmin"] = results[0][0]
    new_dict["Tmax"] = results[0][1]
    new_dict["Tavg"] = results[0][2]

    return jsonify(new_dict)

#     When given the start only, calculate TMIN, TAVG, 
#     and TMAX for all dates greater than and equal to the start date.

#     When given the start and the end date, calculate the TMIN, TAVG, and 
#     TMAX for dates between the start and end date inclusive.

@app.route("/api/v1.0/<start>/<end>")
def calc_temps(start, end):
#     """TMIN, TAVG, and TMAX for a list of dates."""
    start = str(start)
    end = str(end)
    temps = [func.min(measurement.tobs),
            func.max(measurement.tobs),
            func.avg(measurement.tobs)]
#    """Args:
#         start_date (string): A date string in the format %Y-%m-%d
#         end_date (string): A date string in the format %Y-%m-%d
        
#     Returns:
#         TMIN, TAVE, and TMAX
#     """
    session = Session(engine)
    results = session.query(*temps)\
                    .filter(measurement.date >= start)\
                    .filter(measurement.date <= end)\
                    .all()

    new_dict = {}
    new_dict["Tmin"] = results[0][0]
    new_dict["Tmax"] = results[0][1]
    new_dict["Tavg"] = results[0][2]

    return jsonify(new_dict)
    
    
if __name__ == "__main__":
    app.run(debug=True)