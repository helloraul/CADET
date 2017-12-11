""" This is a class defining the REST API interface to access the 'Datasets'
    uploaded to the database. There should be the ability to GET, POST, PUT,
    and DELETE to the 'Datasets' table in the database.
"""

from flask import abort
from flask_restful import Resource, request
from cadetapi.models import ResultSet
from cadetapi.controllers.database.DbControl import DbResult
from cadetapi.controllers.analysis.DatasetAnalysis import DataSetAnalysis

class DatasetApi(Resource):
    def post(self):
        # Receive single comment as json object (primarily for unit testing
        record = DbResult()
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

	
        return response


"""""
 a call to analyze api
       if (record.Query(pk)==false)
           recordValidate.runAnalysis(pk)
        return response
"""""
 
