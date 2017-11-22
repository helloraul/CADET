""" This is a class defining the REST API interface to access the 'Instructors'
    uploaded to the database. There should be the ability to GET, POST, PUT,
    and DELETE to the 'Instructors' table in the database.
"""

from flask import abort
from flask_restful import Resource, marshal_with
from cadetapi.models import Instructor
from .fields import instructor_fields

class InstructorApi(Resource):
    @marshal_with(instructor_fields)
    def get(self, instructor_id=None):
        if instructor_id:
            instructor = Instructor.query.get(instructor_id)
            if not instructor:
                abort(404)
            return instructor
        else:
            instructors = Instructor.query.all()
            return instructors
