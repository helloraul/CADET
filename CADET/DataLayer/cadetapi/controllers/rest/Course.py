""" This is a class defining the REST API interface to access the 'Courses'
    uploaded to the database. There should be the ability to GET, POST, PUT,
    and DELETE to the 'Courses' table in the database.
"""

from flask import abort
from flask_restful import Resource, marshal_with
from cadetapi.models import Course
from .fields import course_fields

class CourseApi(Resource):
    @marshal_with(course_fields)
    def get(self, course_id=None):
        if course_id:
            courses = Course.query.get(course_id)
            if not courses:
                abort(404)
            return courses
        else:
            courses = Course.query.all()
            return courses
