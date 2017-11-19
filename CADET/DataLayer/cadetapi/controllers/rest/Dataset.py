""" This is a class defining the REST API interface to access the 'Datasets'
    uploaded to the database. There should be the ability to GET, POST, PUT,
    and DELETE to the 'Datasets' table in the database.
"""

from flask import abort
from flask_restful import Resource, marshal_with
from cadetapi.models import DataSet
from .fields import dataset_fields

class DatasetApi(Resource):
    @marshal_with(dataset_fields)
    def get(self, dataset_id=None):
        if dataset_id:
            dataset = Dataset.query.get(dataset_id)
            if not dataset:
                abort(404)
            return dataset
        else:
            datasets = Dataset.query.all()
            return datasets
