import unittest
import user


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.usr_mngr = user.UserManager("")

    def test_if_admin_return_true(self):
        new_usr = self.usr_mngr.get_user("admin")
        self.assertTrue(new_usr.is_admin())

    def test_if_not_admin_return_true(self):
        new_usr = self.usr_mngr.get_user("name")
        self.assertTrue(not new_usr.is_admin())

if __name__ == '__main__':
    unittest.main()
