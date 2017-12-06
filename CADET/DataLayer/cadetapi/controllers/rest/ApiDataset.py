""" This is a class defining the REST API interface to access the 'Datasets'
    uploaded to the database. There should be the ability to GET, POST, PUT,
    and DELETE to the 'Datasets' table in the database.
"""

from flask import abort
from flask_restful import Resource, request
#from cadetapi.models import DataSet
from cadetapi.controllers.database.DbControl import DbDataset
from cadetapi.schemas import DatasetSchema

class DatasetApi(Resource):
    def get(self, dataset_id=None):
        # Retrieve datasets from database
        inst = DbDataset()
        response = inst.Query(dataset_id)

        # marshall dataset(s) into dict
        if dataset_id is None:
            result = DatasetSchema(many=True).dump(response).data
        else:
            result = DatasetSchema(many=False).dump(response).data

        # return result dict and 204 code if empty
        if (result):
            return result
        else:
            return result, 204z

    def post(self):
        # Receive single comment as json object (primarily for unit testing)
        record = DbResult()
        recordValidate = DatasetAnalysis()
        req = request.get_json()
        meta = req['meta_file_info']
      
        pk = record.GetId(
                req['raw_file_stats'],
                meta['user_selected_number_topics'],
                meta['user_selected_words_per_topic'],
                meta['user_selected_number_iterations'],
            )
        response = {}
        response['resultset_id'] = pk

"""""
 a call to analyze api
"""""
        if (record.Query(pk)= false) 
           recordValidate.runAnalysis(pk)
        return response


"""
    def get(self, dataset_id=None):
        if dataset_id:
            dataset = DataSet.query.get(dataset_id)
            if not dataset:
                abort(404)
            return dataset
        else:
            datasets = DataSet.query.all()
            return datasets
"""

 
