""" This is a class defining the REST API interface to access the 'Instructors'
    uploaded to the database. There should be the ability to GET from the
    'Instructors' table in the database.
"""

from flask import abort
from flask_restful import Resource, marshal_with
from cadetapi.models import Instructor
from .fields import instructor_fields

class InstrApi(Resource):
    @marshal_with(instructor_fields)
    def get(self, instructor_id=None):
        if instructor_id:
            result = Instructor.query.get(instructor_id)
            if not result:
                abort(404)
            return result
        else:
            result = Instructor.query.all()
            return result
