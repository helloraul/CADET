"""Make sure the TestConfig is being used in __init__.py"""

import os
import cadetapi
import unittest
import json

class TestURLs(unittest.TestCase):
    def setUp(self):
        cadetapi.app.testing = True
        self.client = cadetapi.app.test_client()

    def post_comment(self):
        postdata = json.dumps(dict(anon_id = "42", \
            instructor_first_name = "Joe",      \
            instructor_last_name = "Bennett",   \
            course_program = "Engineering",     \
            course_modality = "in-person",      \
            course_num_sect_id = "605.423",     \
            course_comments = "I like this class overall", \
            instructor_comments = "The instructor did a good job of challenging the students", \
            additional_comments = "The campus is in a really convenient location"))

        return self.client.post('/api/Comment', data=postdata, content_type='application/json')

    def test_root_return(self):
        """Tests if the root URL gives Hello, World"""
        result = self.client.get('/')
        assert result.status_code == 200
        assert "Hello, World" in result.data

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
        result = self.post_comment()
        assert result.status_code == 200
        assert result.headers['Content-Type'] == "application/json"
        assert 'comment_id' in result.data
        result = self.client.get('/api/Comment')
        assert result.status_code == 200
        assert result.headers['Content-Type'] == "application/json"
        assert ""


#    def test_result_return(self):
#        """Tests the Result URL"""
#        # check root result url
#        result = self.client.get('/api/Result')
#        assert result.status_code == 204 # expecting the table to be empty
#        assert result.headers['Content-Type'] == "application/json"
#        # check again with trailing slash
#        result = self.client.get('/api/Result/')
#        assert result.status_code == 204 # expecting the table to be empty
#        assert result.headers['Content-Type'] == "application/json"
#        # check element from Comment
#        result = self.client.get('/api/Result/1')
#        assert result.status_code == 204 # expecting the element to not exist
#        assert result.headers['Content-Type'] == "application/json"

if __name__ == '__main__':
    unittest.main()

