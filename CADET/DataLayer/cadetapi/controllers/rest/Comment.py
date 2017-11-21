""" This is a class defining the REST API interface to access the 'Comments'
    uploaded to the database. There should be the ability to GET, POST, PUT,
    and DELETE to the 'Comments' table in the database.
"""

from flask import abort
from flask_restful import Resource, request
from cadetapi.models import Comment
from cadetapi.controllers.database.cadet_insert import DbComment
from cadetapi.schemas import CommentSchema

class CommentApi(Resource):
    def get(self, comment_id=None):
        inst = DbComment()
        if comment_id is None:
            # No ID was provided, so we'll return everything
            comments = inst.GetAll()
            return CommentSchema(many=True).load(comments)
        else:
            # Specific Comment was requested by ID
            comment = inst.GetComment(comment_id)
            if not comment:
                abort(404)
            return CommentSchema().load(comment)

    def post(self):
        # Receive single comment as json object (primarily for unit testing)
        NewComment = DbComment()
        response = {}
        response['comment_id'] = NewComment.GetId(request.get_json())
        return response
