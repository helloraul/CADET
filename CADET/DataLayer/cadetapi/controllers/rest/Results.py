""" This is a class defining the REST API interface to access the 'Results'
    uploaded to the database. There should be the ability to GET, POST, PUT,
    and DELETE to the 'Results' table in the database.
"""

from flask import abort
from flask_restful import Resource, marshal_with
from cadetapi.models import Result
from .fields import results_fields


class ResultApi(Resource):
    @marshal_with(results_fields)
    def get(self, result_id=None):
        if result_id:
            result = Result.query.get(result_id)
            if not result:
                abort(404)
            return result
        else:
            results = Result.query.all()
            return results
