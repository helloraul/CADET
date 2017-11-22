""" This is a class defining the REST API interface to access the 'Courses'
    uploaded to the database. There should be the ability to GET, POST, PUT,
    and DELETE to the 'Courses' table in the database.
"""

from flask import abort
from flask_restful import Resource, marshal_with
from cadetapi.models import Course
from cadetapi.controllers.database.cadet_insert import DbCourse
from cadetapi.schemas import CourseSchema

class CourseApi(Resource):
    def get(self, course_id=None):
        inst = DbCourse()
        response = inst.Query(course_id)
        if course_id is None:
            return CourseSchema(many=True).dump(response).data
        else:
            return CourseSchema(many=False).dump(response).data
