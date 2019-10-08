import unittest

class TestStringMethods2(unittest.TestCase):
    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')
        
class TestStringMethods(unittest.TestCase):
    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('foo'.isupper())

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestStringMethods))
    suite.addTest(unittest.makeSuite(TestStringMethods2))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())