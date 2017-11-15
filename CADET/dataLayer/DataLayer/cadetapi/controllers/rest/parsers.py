""" These define the arguments expected when calling one of the APIs. More
    information can be found at:
    https://flask-restful.readthedocs.io/en/0.3.6/reqparse.html
"""

from flask_restful import reqparse

analysis_post_parser = reqparser.RequestParser()
analysis_post_parser.add_argument(
    'anon_id',
    type=int,
    location=['json'],
    required=true
)
#'program' string
#'modality' int
#'course_num_sect_id' string
#'instructor_last_name' string
#'instructor_first_name' string
#'course_comments' string
#'instructor_comments' string
#'additional_comments' string
