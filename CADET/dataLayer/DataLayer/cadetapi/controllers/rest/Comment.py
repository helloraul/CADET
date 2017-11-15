""" This is a class defining the REST API interface to access the 'Comments'
    uploaded to the database. There should be the ability to GET, POST, PUT,
    and DELETE to the 'Comments' table in the database.
"""

from flask import abort
from flask_restful import Resource, marshal_with
from cadetapi.models import Comment
from .fields import comment_fields

class CommentApi(Resource):
    @marshal_with(comment_fields)
    def get(self, comment_id=None):
        if comment_id:
            comment = Comment.query.get(comment_id)
            if not comment:
                abort(404)
            return comment
        else:
            comments = Comment.query.all()
            return comments
