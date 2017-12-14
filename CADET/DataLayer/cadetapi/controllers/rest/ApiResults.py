""" This is a class defining the REST API interface to access the 'Results'
    uploaded to the database. There should be the ability to GET the 'Results'
    table in the database.
"""

from flask import abort
from flask_restful import Resource, request
from ..database.DbControl import DbResult
from ...schemas import ResultSchema

class ResultApi(Resource):
    def get(self, result_id=None):
        if (result_id is not None):
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
        else:
            result = dict(error = "Method requires ID to be specified")
            return result, 405
