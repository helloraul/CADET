""" Make sure the TestConfig is being used in __init__.py"""
""" Dump into json, load from json """

from cadetapi.schemas import *
import unittest
import json
from test_vectors import *

class TestSchemas(unittest.TestCase):

    def test_commentSchema(self):
        """CommentSchema Dump Test"""
        schema = CommentSchema()
        temp = schema.dump(CommentExample1).data
        assert 'anon_id' in temp
        assert 'instructor_first_name' in temp
        assert 'course_num_sect_id' in temp

    def test_courseSchema(self):
        """CourseSchema Dump Test"""
        schema = CourseSchema()
        temp = schema.dump(CourseExample1).data
        assert 'course_program' in temp
        assert 'course_modality' in temp
        assert 'course_num_sect_id' in temp

    def test_instructorSchema(self):
        """InstructorSchema Dump Test"""
        schema = InstructorSchema()
        temp = schema.dump(InstructorExample1).data
        assert 'instructor_first_name' in temp
        assert 'instructor_last_name' in temp

    def test_datasetSchema(self):
        """DatasetSchema Dump Test"""
        schema = DatasetSchema()
        temp = schema.dump(DatasetExample).data
        assert 'meta_file_info' in temp
        assert 'raw_file_stats' in temp
        assert 'document_id_number' in temp['meta_file_info']
        assert 'user_selected_words_per_topic' in temp['meta_file_info']
        for comment in temp['raw_file_stats']:
            assert 'anon_id' in comment
            assert 'program' in comment
            assert 'additional_comments' in comment
            assert 'modality' in comment

    def test_datasetSchema_load(self):
        """Load DatasetSchema Test"""
        schema = DatasetSchema()
        temp = schema.dump(DatasetExample).data
        temp = schema.load(temp).data
        assert 'meta_file_info' in temp
        assert 'raw_file_stats' in temp
        assert 'document_id_number' not in temp['meta_file_info']
        assert 'user_selected_words_per_topic' in temp['meta_file_info']
        for comment in temp['raw_file_stats']:
            assert 'anon_id' in comment
            assert 'program' in comment
            assert 'additional_comments' in comment
            assert 'modality' in comment

    def test_ResultTopicSchema(self):
        """ResultTopicSchema Dump Test"""
        schema = ResultTopicSchema()
        temp = schema.dump(ResultTopicExample).data
        assert 'words' in temp
        assert 'comments' in temp

        comments = temp['comments']
        assert 'positive' in comments
        assert 'negative' in comments
        assert 'neutral' in comments


    def test_resultSchema(self):
        """ResultSchema Dump Test"""
        schema = ResultSchema()
        temp = schema.dump(ResultExample).data
        assert 'result_id' in temp
        assert 'meta_file_info' in temp
        assert 'results' in temp
        assert 'document_id_number' in temp['meta_file_info']
        assert 'user_selected_words_per_topic' in temp['meta_file_info']
        results = temp['results']
        assert 'topic_stats' in temp['results']
        topiclist = results['topic_stats']
        for topic in topiclist:
            assert 'words' in topic
            assert 'comments' in topic
            sentim = topic['comments']
            assert 'positive' in sentim
            assert 'negative' in sentim
            assert 'neutral' in sentim
        assert 'instructor_stats' in temp['results']
        instrlist = results['instructor_stats']
        for instr in instrlist:
            assert 'instructor_first' in instr
            assert 'instructor_last' in instr
            assert 'course_num_sect_id' in instr
            assert 'comments' in instr
            # with instr['comments'] as sentim:
            sentim = instr['comments']
            assert 'positive' in sentim
            assert 'negative' in sentim
            assert 'neutral' in sentim




if __name__ == '__main__':
    unittest.main()

