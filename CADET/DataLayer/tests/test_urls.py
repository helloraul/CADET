"""Make sure the TestConfig is being used in __init__.py"""

import os
from test_vectors import *
from cadetapi.schemas import *
import cadetapi
import unittest
import json

# in python3, need to change strings to bytes, and dont forget to supply an encoding
def isStringIn(s, obj):
    return bytes(s, encoding='utf8') in obj


def post_comment(client):
    senddata = CommentSchema().dump(CommentExample1).data
    return client.post('/api/Comment', data=senddata, content_type='application/json')


def post_dataset(client):
    senddata = DatasetSchema().dump(DatasetExample).data
    print(senddata)
    return client.post('/api/Dataset/', data=senddata, content_type='application/json')


class TestURLs(unittest.TestCase):
    def setUp(self):
        cadetapi.app.testing = True
        self.client = cadetapi.app.test_client()

    def test_root_return(self):
        """Tests if the root URL gives Hello, World"""
        result = self.client.get('/')
        assert result.status_code == 200
        assert isStringIn("Hello, World", result.data)


    def test_comment_return(self):
        """Tests the Comment URL"""
        # check root comment url
        result = self.client.get('/api/Comment')
        assert result.status_code == 204 # expecting the table to be empty
        assert result.headers['Content-Type'] == "application/json"
        # check again with trailing slash
        result = self.client.get('/api/Comment/')
        assert result.status_code == 204 # expecting the table to be empty
        assert result.headers['Content-Type'] == "application/json"
        # check element from Comment
        result = self.client.get('/api/Comment/1')
        assert result.status_code == 204 # expecting the element to not exist
        assert result.headers['Content-Type'] == "application/json"
        # post data to comment table
        result = post_comment(self.client)
        assert result.status_code == 201
        assert result.headers['Content-Type'] == "application/json"
        assert isStringIn("comment_id", result.data)
        # check comment in database
        result = self.client.get('/api/Comment')
        assert result.status_code == 200
        assert result.headers['Content-Type'] == "application/json"
        assert isStringIn("anon_id", result.data)
        assert isStringIn("course_num_sect_id", result.data)
        assert isStringIn("additional_comments", result.data)
        # check comment in database specifying element
        result = self.client.get('/api/Comment/1')
        assert result.status_code == 200
        assert result.headers['Content-Type'] == "application/json"
        assert isStringIn("anon_id", result.data)
        assert isStringIn("course_num_sect_id", result.data)
        assert isStringIn("additional_comments", result.data)

    def test_dataset(self):
        """Tests the Dataset URL"""
        # check root dataset url
        result = self.client.get('/api/Dataset')
        assert result.status_code == 405 # expecting error
        assert result.headers['Content-Type'] == "application/json"
        # check again with trailing slash
        result = self.client.get('/api/Dataset/')
        assert result.status_code == 405 # expecting error
        assert result.headers['Content-Type'] == "application/json"
        # check element from Comment
        result = self.client.get('/api/Dataset/1')
        assert result.status_code == 204 # expecting the element to not exist
        assert result.headers['Content-Type'] == "application/json"
        # post data to comment table
        result = post_dataset(self.client)
        assert result.status_code == 201
        assert result.headers['Content-Type'] == "application/json"
        assert isStringIn("resultset_id", result.data)
        # check comment in database
        result = self.client.get('/api/Dataset')
        print(result.data, result.status_code)
        assert result.status_code == 200
        assert result.headers['Content-Type'] == "application/json"
        assert "anon_id" in result.data
        assert "course_num_sect_id" in result.data
        assert "additional_comments" in result.data
        # check comment in database specifying element
        result = self.client.get('/api/Dataset/1')
        print(result.data, result)
        assert result.status_code == 200
        assert result.headers['Content-Type'] == "application/json"
        assert "anon_id" in result.data
        assert "course_num_sect_id" in result.data
        assert "additional_comments" in result.data

    # code commented out for future enhancement and tests for comprhensive
    # coverage of the application.
   # def test_result_return(self):
       # """Tests the Result URL"""
       # # check root result url
       # result = self.client.get('/api/Result')
       # assert result.status_code == 204 # expecting the table to be empty
       # assert result.headers['Content-Type'] == "application/json"
       # # check again with trailing slash
       # result = self.client.get('/api/Result/')
       # assert result.status_code == 204 # expecting the table to be empty
       # assert result.headers['Content-Type'] == "application/json"
       # # check element from Comment
       # result = self.client.get('/api/Result/1')
       # assert result.status_code == 204 # expecting the element to not exist
       # assert result.headers['Content-Type'] == "application/json"

if __name__ == '__main__':
    unittest.main()

