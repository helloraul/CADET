""" This is a class defining the REST API interface to access the 'Instructors'
    uploaded to the database. There should be the ability to GET, POST, PUT,
    and DELETE to the 'Instructors' table in the database.
"""

from flask import abort
from flask_restful import Resource, request
from cadetapi.models import Instructor
from cadetapi.controllers.database.cadet_insert import DbInstructor
from cadetapi.schemas import InstructorSchema

class InstructorApi(Resource):
    def get(self, instr_id=None):
        # Retrieve instructors from database
        inst = DbInstructor()
        response = inst.Query(instr_id)

        # marshall instructor(s) into dict
        if instr_id is None:
            result = InstructorSchema(many=True).dump(response).data
        else:
            result = InstructorSchema(many=False).dump(response).data

        # return result dict and 204 code if empty
        if (result):
            return result
        else:
            return result, 204

