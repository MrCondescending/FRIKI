import unittest
from wiki.core import Page
from Friki import app
from wiki.web import current_wiki

class MyTestCase(unittest.TestCase):
    def setUp(self):
        app.config['Testing'] = True
        app.config['DEBUG'] = False
        self.assertEqual(app.debug, False)

    def tearDown(self) :
        pass


    def test_tagsApiCall(self):
        c = app.test_client()
        response = c.get('/tags', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_tagApiCall(self):
        c = app.test_client()
        response = c.get('/tag/', follow_redirects=True)
        print(response)
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
