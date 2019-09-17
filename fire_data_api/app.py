"""
Module to pull fire data from the MODUS project for use in Fire Flight.

User can send coordinates to API along with a perimiter value (in miles) and receive
an alert if there are active fires within that perimter.
"""

# Flask App Imports
from flask import Flask 
from flask_restful import Api, reqparse
from flask_cors import CORS
from json import dumps



# Database imports
from .models import db, Fire
import os

from .resources import CheckFires, AllFires

# Different schedulers for querying data
from apscheduler.schedulers.background import BackgroundScheduler
# import schedule, time


# data source
# https://earthdata.nasa.gov/earth-observation-data/near-real-time/firms
# website home for modis and viirs data

def create_app():
    """
    Creates and configures an instance of our Flask API
    """
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["ENV"] = os.environ.get("ENV") #apparently this doesn't really work so commenting out for now
    db.init_app(app)


    # enable CORS on all app routes
    CORS(app)

    #initialize the api wrapper
    api = Api(app)

    # connects resources to api endpoint
    api.add_resource(CheckFires, "/check_fires")
    api.add_resource(AllFires, "/all_fires")



        
    # # pulls a new df every hour
    # scheduler = BackgroundScheduler()
    # scheduler.add_job(check_new_df, 'interval', hours=1)
    # scheduler.start()

    # # manually update csv
    # @app.route('/data/update', methods=['GET'])
    # def check_modus_data():
    #     new_df = check_new_df()
    #     size = new_df.shape
    #     global df
    #     df = new_df

    #     return jsonify({'new df size ': size}), 201

    # # check our df size
    # @app.route('/data/size', methods=['GET'])
    # def df_size():
    #     size = df.shape
    #     return jsonify({'df_size' : size}), 201

    # # check our df head
    # @app.route('/data/head', methods=['GET'])
    # def df_head():
    #     head = df.head().to_json()
    #     return jsonify({'df_head' : head}), 201

    return app
