"""
API Resources.
"""

from flask import jsonify, request
from flask_restful import Resource
from .functions import check_fires

class CheckFires(Resource):
    """
    Get's User long/lat coordinates and returns a json
    """

    def post(self):
        values = request.get_json()

        user_coords = values['user_coords'] #I want to get a json like:
        #{'user_coords' : (long, lat), 'distance': number} 
        try:
            perimiter = values['distance']
        except:
            perimiter = 50

        #get's all high confidence fire coords from our df
        fire_coords = df.loc[df['confidence'] > 90][['longitude', 'latitude']].values

        return jsonify(check_fires(user_coords, perimiter, fire_coords))


class AllFires(Resource):
    """
    Returns a json with all active fires
    """

    def get(self):
        
        #get all fire coords
        fire_coords = df.loc[df['confidence'] > 90][['longitude', 'latitude']].values

        results = {
            'Alert' : True,
            'Fires' : [tuple(x) for x in fire_coords]
        }

        return jsonify(results)