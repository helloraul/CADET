""" This is a class defining the REST API interface to access the 'Datasets'
    uploaded to the database. There should be the ability to GET, POST, PUT,
    and DELETE to the 'Datasets' table in the database.
"""

from flask import abort
from flask_restful import Resource, request
from ...models import ResultSet
from ...schemas import CommentSchema
from ..database.DbControl import DbResult
from ..database.DbControl import DbDataset
from ..analysis.DatasetAnalysis import DatasetAnalysis

class DatasetApi(Resource):
    def get(self, dataset_id=None):
        if (dataset_id is not None):
            # Retrieve dataset from database
            inst = DbDataset()
            response = inst.Query(dataset_id)

            # marshall dataset into dict
            result = CommentSchema(many=True).dump(response).data

            # return result dict and 204 code if empty
            if (result):
                return result
            else:
                return result, 204
        else:
            result = dict(error = "Method requires ID to be specified")
            return result, 405

    def post(self):
        # Receive single comment as json object (primarily for unit testing
        record = DbResult()
        req = request.get_json(force=True)
        meta = req['meta_file_info']
        pk = record.GetId(
                req['raw_file_stats'],
                meta['user_selected_number_topics'],
                meta['user_selected_words_per_topic'],
                meta['user_selected_number_iterations'],
            )
        recordValidate = DatasetAnalysis(pk)
        response = {}

        response['resultset_id'] = pk

        if (record.Query(pk)==False):
            recordValidate.runAnalysis()

        return response
