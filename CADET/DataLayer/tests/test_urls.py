"""Make sure the TestConfig is being used in __init__.py"""

import os
import cadetapi
import unittest
import json

# in python3, need to change strings to btyes, and dont forget to supply an encoding
def isStringIn(s, obj):
    return bytes(s, encoding='utf8') in obj

class TestURLs(unittest.TestCase):
    def setUp(self):
        cadetapi.app.testing = True
        self.client = cadetapi.app.test_client()

    def post_comment(self):
        postdata = json.dumps(dict(
            anon_id = "42", \
            instructor_first_name = "Joe",      \
            instructor_last_name = "Bennett",   \
            course_program = "Engineering",     \
            course_modality = "in-person",      \
            course_num_sect_id = "605.423",     \
            course_comments = "I like this class overall", \
            instructor_comments = "The instructor did a good job of challenging the students", \
            additional_comments = "The campus is in a really convenient location"))

        return self.client.post('/api/Comment', data=postdata, content_type='application/json')

    def post_dataset(self):
        postdata = json.dumps(dict(
            meta_file_info = dict(
                document_id_number = "3",
                user_selected_words_per_topic = "5",
                user_selected_number_topics = "4",
                user_selected_number_iterations = "30"
            ),
        raw_file_stats = [
            dict(
                anon_id = "12",
                program = "Computer Science",
                modality = "classroom",
                course_num_sect_id = "604.211",
                instructor_last_name = "Coffman",
                instructor_first_name = "Joel",
                course_comments = "course comment 1",
                instructor_comments = "instructor comment 1",
                additional_comments = "additional comment 1"
            ),
            dict(
                anon_id = "23",
                program = "Computer Science",
                modality = "classroom",
                course_num_sect_id = "604.211",
                instructor_last_name = "Coffman",
                instructor_first_name = "Joel",
                course_comments = "course comment 2",
                instructor_comments = "instructor comment 2",
                additional_comments = "additional comment 2"
            ),
            dict(
                anon_id = "42",
                program = "Computer Science",
                modality = "classroom",
                course_num_sect_id = "604.211",
                instructor_last_name = "Coffman",
                instructor_first_name = "Joel",
                course_comments = "course comment 3",
                instructor_comments = "instructor comment 3",
                additional_comments = "additional comment 3"
            )]))

        return self.client.post('/api/Dataset/', data=postdata, content_type='application/json')

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
        result = self.post_comment()
        assert result.status_code == 200
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
#        # check root dataset url
#        result = self.client.get('/api/dataset')
#        assert result.status_code == 204 # expecting the table to be empty
#        assert result.headers['Content-Type'] == "application/json"
#        # check again with trailing slash
#        result = self.client.get('/api/Comment/')
#        assert result.status_code == 204 # expecting the table to be empty
#        assert result.headers['Content-Type'] == "application/json"
#        # check element from Comment
#        result = self.client.get('/api/Comment/1')
#        assert result.status_code == 204 # expecting the element to not exist
#        assert result.headers['Content-Type'] == "application/json"
#        # post data to comment table
        result = self.post_dataset()
        print(result.status_code)
        assert result.status_code == 201
        assert result.headers['Content-Type'] == "application/json"
        assert isStringIn("result_id", result.data)
#        # check comment in database
#        result = self.client.get('/api/Comment')
#        assert result.status_code == 200
#        assert result.headers['Content-Type'] == "application/json"
#        assert "anon_id" in result.data
#        assert "course_num_sect_id" in result.data
#        assert "additional_comments" in result.data
#        # check comment in database specifying element
#        result = self.client.get('/api/Comment/1')
#        assert result.status_code == 200
#        assert result.headers['Content-Type'] == "application/json"
#        assert "anon_id" in result.data
#        assert "course_num_sect_id" in result.data
#        assert "additional_comments" in result.data


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

