""" This file defines the RESTful API endpoints and which URL to use to
    connect to them. This file also creates the rest_api object initialized
    with the rest of the web application.
    For more information please refer to:
    https://flask-restful.readthedocs.io/en/latest/
"""
from flask_restful import Api
from .controllers.rest.ApiComment import CommentApi
from .controllers.rest.ApiCourse import CourseApi
from .controllers.rest.ApiInstructor import InstructorApi
from .controllers.rest.ApiDataset import DatasetApi
from .controllers.rest.ApiResults import ResultApi

rest_api = Api()


rest_api.add_resource(
    CommentApi,                       # name of class handling requests
    '/api/Comment',                   # url to retrieve table
    '/api/Comment/<int:comment_id>',  # url to retrieve elements in table
    '/api/Comment/',                  # alt url to retrieve table
    '/api/Comment/<int:comment_id>/', # alt url to retrieve elements in table
    endpoint='comment'                # Flask name of API endpoint
    )

rest_api.add_resource(
    CourseApi,                        # name of class handling requests
    '/api/Course',                    # url to retrieve table
    '/api/Course/<int:course_id>',    # url to retrieve elements in table
    '/api/Course/',                   # alt url to retrieve table
    '/api/Course/<int:course_id>/',   # alt url to retrieve elements in table
    endpoint='course'                 # Flask name of API endpoint
    )

rest_api.add_resource(
    InstructorApi,                    # name of class handling requests
    '/api/Instructor',                # url to retrieve table
    '/api/Instructor/<int:instr_id>' ,# url to retrieve elements in table
    '/api/Instructor/',               # alt url to retrieve table
    '/api/Instructor/<int:instr_id>/',# alt url to retrieve elements in table
    endpoint='instr'                  # Flask name of API endpoint
    )

rest_api.add_resource(
    DatasetApi,                       # name of class handling requests
    '/api/Dataset',                   # url to retrieve table
    '/api/Dataset/<int:dataset_id>',  # url to retrieve elements in table
    '/api/Dataset/',                  # alt url to retrieve table
    '/api/Dataset/<int:dataset_id>/', # alt url to retrieve elements in table
    endpoint='dataset'                # Flask name of API endpoint
    )

rest_api.add_resource(
    ResultApi,                        # name of class handling requests
    '/api/Result',                    # url to retrieve table
    '/api/Result/<int:result_id>',    # url to retrieve elements in table
    '/api/Result/',                   # alt url to retrieve table
    '/api/Result/<int:result_id>/',   # alt url to retrieve elements in table
    endpoint='result'                 # Flask name of API endpoint
    )

