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
    program = field_for(Course, 'program', dump_only=True)
    modality = field_for(Course, 'modality', dump_only=True)
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
    instructor_first_name = field_for(Instructor, 'first_name', dump_only=True)
    instructor_last_name = field_for(Instructor, 'last_name', dump_only=True)

class StopwordSchema(ModelSchema):
    word_id = field_for(Stopword, 'id', dump_only=True)
    stop_word = field_for(Stopword, 'stop_word', dump_only=True)

class MetaSchema(ModelSchema):
    document_id_number = ma.Integer(dump_only=True)
    user_selected_number_topics = ma.Integer()
    user_selected_number_iterations = ma.Integer()
    user_selected_words_per_topic = ma.Integer()

class CommentSentimentSchema(ModelSchema):
    positive = ma.List(ma.String())
    neutral = ma.List(ma.String())
    negative = ma.List(ma.String())

class DatasetSchema(ModelSchema):
    meta_file_info = ma.Nested(MetaSchema)
    raw_file_stats = ma.Nested(CommentSchema, many=True)

class ResultTopicSchema(ModelSchema):
    words = ma.List(ma.String())
    comments = ma.Nested(CommentSentimentSchema)

class ResultInstructorSchema(ModelSchema):
    instructor_first = ma.String()
    instructor_last  = ma.String()
    course_num_sect_id = ma.String()
    comments = ma.Nested(CommentSentimentSchema)

class ResultSchema(ModelSchema):
    result_id = ma.Integer()
    meta_file_info = ma.Nested(MetaSchema)
    results = {}
    results['topic_stats'] = ma.Nested(ResultTopicSchema, many=True)
    results['instructor_stats'] = ma.Nested(ResultInstructorSchema, many=True)

