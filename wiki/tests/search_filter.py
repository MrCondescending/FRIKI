import unittest
from unittest.mock import patch
import wiki.web
import user
from Friki import app

class MyTestCase(unittest.TestCase):
    def test(self):
        self.app = app.test_client()
        self.app.testing = True
        result = self.app.get('/search/filter/')
        c = self.app.post('/search/filter')
        self.assertEqual(result.status_code, 302)

if __name__ == '__main__':
    unittest.main()
