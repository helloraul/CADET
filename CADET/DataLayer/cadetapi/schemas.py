""" These classes define the return values from the appropriate API calls.
    Marshmellow is used to serialize/deserialize the data between json and
    other python objects.
    More information can be found below:
    https://marshmallow.readthedocs.io/en/latest/
"""

from flask_marshmallow import Marshmallow
from marshmallow_sqlalchemy import ModelSchema, field_for
from .models import *

ma=Marshmallow()

class CommentSchema(ModelSchema):
    anon_id = field_for(Comment, 'anon_id', dump_only=True)
    course_program = field_for(Course, 'program', dump_only=True)
    course_modality = field_for(Course, 'modality', dump_only=True)
    course_num_sect_id = field_for(Course, 'num_sec', dump_only=True)
    instructor_first_name = field_for(Instructor, 'first_name', dump_only=True)
    instructor_last_name = field_for(Instructor, 'last_name', dump_only=True)
    course_comments = field_for(Comment, 'c_com', dump_only=True)
    instructor_comments = field_for(Comment, 'i_com', dump_only=True)
    additional_comments = field_for(Comment, 'a_com', dump_only=True)

class CourseSchema(ModelSchema):
    course_program = field_for(Course, 'program', dump_only=True)
    course_modality = field_for(Course, 'modality', dump_only=True)
    course_num_sect_id = field_for(Course, 'num_sec', dump_only=True)

class InstructorSchema(ModelSchema):
    stub = 'need to do this'

class DatasetSchema(ModelSchema):
    stub = 'need to do this'

class ResultSchema(ModelSchema):
    stub = 'need to do this'
