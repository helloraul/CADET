import os
import cadetapi
import unittest
import tempfile

class TestURLs(unittest.TestCase):
    def setUp(self):
        self.db_fd, cadetapi.app.config['DATABASE'] = tempfile.mkstemp()
        cadetapi.app.testing = True
        self.app = cadetapi.app.test_client()
        with cadetapi.app.app_context():
            cadetapi.init_db

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(cadetapi.app.config['DATABASE'])

    def test_root_return(self):
        """Tests if the root URL gives Hello, World"""
        result = self.client.get('/')
        assert result.status_code == 200
        assert "Hello, World" in result.body

    def test_comment_return(self):
        """Tests the Comment URL"""
        # check root comment url
        result = self.client.get('/api/Comment')
        assert result.status_code == 200
        assert "application/json" in result.header
        assert "{" in result.body
        # check again with trailing slash
        result = self.client.get('/api/Comment/')
        assert result.status_code == 200
        assert "application/json" in result.header
        assert "{" in result.body
        # check element from Comment
        result = self.client.get('/api/Comment/1')
        assert result.status_code == 200
        assert "application/json" in result.header
        assert "anon_id" in request.body
        # check non-existing element
        result = self.client.get('/api/Comment/1337')
        assert result.status_code == 204
        assert "application/json" in result.header

if __name__ == '__main__':
    unittest.main()
