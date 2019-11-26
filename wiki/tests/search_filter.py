import unittest
import os


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.usr_mgr = user.UserManager('../tests/')


if __name__ == '__main__':
    unittest.main()
