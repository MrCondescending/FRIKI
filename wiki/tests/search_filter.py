import unittest
from Friki import app


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def tearDown(self):
        pass

    def test_filter_get_redirect(self):
        result = self.app.get('/search/filter/')
        self.assertEqual(result.status_code, 302)

    def test_filter_post_redirect(self):
        result = self.app.post('/search/filter')
        self.assertEqual(result.status_code, 308)


if __name__ == '__main__':
    unittest.main()
