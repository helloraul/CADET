""" These classes define the return values from the appropriate API calls.
    Marshmellow is used to serialize/deserialize the data between json and
    other python objects.
    More information can be found below:
    https://marshmallow.readthedocs.io/en/latest/
"""

from flask_marshmallow import Marshmallow, fields

ma=Marshmallow()

class CommentSchema(ma.Schema):
    #comment_id = ma.fields.Integer(attribute='id')
    anon_id = ma.Integer()
    instructor_first_name = ma.String()
    instructor_last_name = ma.String()
    course_program = ma.String()
    course_modality = ma.String()
    course_num_sect_id = ma.String()
    course_comments = ma.String()
    instructor_comments = ma.String()
    additional_comments = ma.String()
    #additional_comment = ma.String(attribute='a_com')
    