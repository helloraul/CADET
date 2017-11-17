import unittest

class TestURLs(unittest.TestCase):
    def setUp(self):
        #Bug workaround
        admin._views = []
        rest_api.resources = []

        app = create_app('webapp.config.TestConfig')
        self.client = app.test_client()

        db.app = app

        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_root_return(self):
        """Tests if the root URL gives Hello, World"""
        result = self.client.get('/')
        assert result.status_code == 200
        assert "Hello, World" in result.body

if __name__ == '__main__':
    unittest.main()
