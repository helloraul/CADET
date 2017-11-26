""" This is a class defining the REST API interface to access the 'Instructors'
    uploaded to the database. There should be the ability to GET, POST, PUT,
    and DELETE to the 'Instructors' table in the database.
"""

from flask import abort
from flask_restful import Resource, request
from cadetapi.models import Stopword
from cadetapi.controllers.database.cadet_insert import DbStopword
from cadetapi.schemas import StopwordSchema

class StopwordApi(Resource):
    def get(self, word_id=None):
        inst = DbStopword()
        response = inst.Query(word_id)
        if word_id is None:
            return StopwordSchema(many=True).dump(response).data
        else:
            return StopwordSchema(many=False).dump(response).data

    def post(self):
        inst = DbStopword()
        response = inst.InsertWord(request.get_json())
        return StopwordSchema(many=True).dump(response).data
