""" This is a class defining the REST API interface to access the 'Results'
    uploaded to the database. There should be the ability to GET, POST, PUT,
    and DELETE to the 'Results' table in the database.
"""

from flask import abort
from flask_restful import Resource, request
from cadetapi.models import ResultSet
from cadetapi.controllers.database.cadet_insert import DbResult
from cadetapi.schemas import ResultSchema

class ResultApi(Resource):
    def get(self, result_id=None):
        if result_id:
            result = ResultSet.query.get(result_id)
            if not result:
                abort(404)
            return result
        else:
            results = ResultSet.query.all()
            return results
