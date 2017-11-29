""" This is a class defining the REST API interface to access the 'Results'
    uploaded to the database. There should be the ability to GET, POST, PUT,
    and DELETE to the 'Results' table in the database.
"""

from flask import abort
from flask_restful import Resource, request
from cadetapi.models import ResultSet
from cadetapi.controllers.database.DbControl import DbResult
from cadetapi.schemas import ResultSchema

class ResultApi(Resource):
    def get(self, result_id=None):
        # Retrieve results from database
        inst = DbResult()
        response = inst.Query(result_id)

        # marshall result(s) into dict
        if result_id is None:
            result = ResultSchema(many=True).dump(response).data
        else:
            result = ResultSchema(many=False).dump(response).data

        # return result dict and 204 code if empty
        if (result):
            return result
        else:
            return result, 204

"""
    def get(self, result_id=None):
        if result_id:
            result = ResultSet.query.get(result_id)
            if not result:
                abort(404)
            return result
        else:
            results = ResultSet.query.all()
            return results
"""
