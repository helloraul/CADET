""" This is a class defining the REST API interface to access the 'Results'
    uploaded to the database. There should be the ability to GET, POST, PUT,
    and DELETE to the 'Results' table in the database.
"""

from flask import abort
from flask_restful import Resource, request
#from cadetapi.models import ResultSet
from cadetapi.controllers.database.DbControl import DbResult
from cadetapi.schemas import ResultSchema

class ResultApi(Resource):
    def get(self, result_id=None):
        # Retrieve results from database
        inst = DbResult()
        response = inst.Query(result_id)

        # marshall result(s) into dict
        if result_id is None:
            result = ResultSchema(many=True).dump(response).data
        else:
            result = ResultSchema(many=False).dump(response).data

        # return result dict and 204 code if empty
        if (result):
            return result
        else:
            return result, 204

    def createFauxResult(self):
        result = {}
        result['meta'] = {}
        result['meta']['doc_id'] = 99
        result['meta']['topics'] = 5
        result['meta']['iterations'] = 100
        result['meta']['words_per_topic'] = 5
        result['topic_stats'] = []
        topicdict = {}
        topicdict['topic_id'] = 1
        topicdict['topic_words'] = ['Alpha', 'Beta', 'Delta', 'Gamma', 'Iota']
        topicdict['positive'] = ['Alpha', 'Gamma']
        topicdict['neutral'] = ['Iota']
        topicdict['negative'] = ['Beta', 'Delta']
        result['topic_stats'].append(topicdict)
        topicdict = {}
        topicdict['topic_id'] = 2
        topicdict['topic_words'] = ['Red', 'Blue', 'Green', 'Orange', 'Yellow']
        topicdict['positive'] = ['Red', 'Yellow']
        topicdict['neutral'] = ['Purple']
        topicdict['negative'] = ['Blue', 'Green', 'Brown']
        result['topic_stats'].append(topicdict)
        topicdict = {}
        topicdict['topic_id'] = 3
        topicdict['topic_words'] = ['one', 'two', 'three', 'four', 'five']
        topicdict['positive'] = ['seven', 'thirteen', 'eleven']
        topicdict['neutral'] = ['twenty']
        topicdict['negative'] = ['Green', 'Iota']
        result['topic_stats'].append(topicdict)
        result['instructor_stats'] = []
        ratingdict = {}
        ratingdict['course_sect'] = '605.101'
        ratingdict['instr_first'] = 'Clark'
        ratingdict['instr_last'] = 'Kent'
        ratingdict['positive'] = ['one', 'two', 'three', 'four', 'five']
        ratingdict['neutral'] = ['Red', 'Blue', 'Green', 'Orange', 'Yellow']
        ratingdict['negative'] = ['Alpha', 'Beta', 'Delta', 'Gamma', 'Iota']
        result['instructor_stats'].append(ratingdict)
        ratingdict = {}
        ratingdict['course_sect'] = 'Course of Solitude'
        ratingdict['instr_first'] = 'Clark'
        ratingdict['instr_last'] = 'Kent'
        ratingdict['positive'] = ['one', 'two', 'three', 'four', 'five']
        ratingdict['neutral'] = ['Red', 'Blue', 'Green', 'Orange', 'Yellow']
        ratingdict['negative'] = ['Alpha', 'Beta', 'Delta', 'Gamma', 'Iota']
        result['instructor_stats'].append(ratingdict)
        ratingdict = {}
        ratingdict['course_sect'] = 'Software Design Principles'
        ratingdict['instr_first'] = 'Joel'
        ratingdict['instr_last'] = 'Coffman'
        ratingdict['positive'] = ['one', 'two', 'three', 'four', 'five']
        ratingdict['neutral'] = ['Red', 'Blue', 'Green', 'Orange', 'Yellow']
        ratingdict['negative'] = ['Alpha', 'Beta', 'Delta', 'Gamma', 'Iota']
        result['instructor_stats'].append(ratingdict)
        return result


"""
    def get(self, result_id=None):
        if result_id:
            result = ResultSet.query.get(result_id)
            if not result:
                abort(404)
            return result
        else:
            results = ResultSet.query.all()
            return results
"""
