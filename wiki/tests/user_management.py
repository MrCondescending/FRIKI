import unittest
import user


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.usr_mng = user.UserManager('../tests/')

    def test_if_admin_return_true(self):
        new_usr = self.usr_mng.get_user("admin")
        self.assertTrue(new_usr.is_admin())

    def test_if_not_admin_return_true(self):
        new_usr = self.usr_mng.get_user("name")
        self.assertTrue(not new_usr.is_admin())

    def test_if_edit_non_admin_then_admin(self):
        modified_user = self.usr_mng.get_user('sam')
        self.usr_mng.edit_user(modified_user.get_id(), modified_user.get('password'), True)
        modified_user = self.usr_mng.get_user('sam')
        self.assertTrue(modified_user.is_admin())

    def test_if_edit_admin_non_admin(self):
        modified_user = self.usr_mng.get_user('sam')
        self.usr_mng.edit_user(modified_user.get_id(), modified_user.get('password'), False)
        modified_user = self.usr_mng.get_user('sam')
        self.assertTrue(modified_user.is_admin() is False)

    def test_if_updated_password_written(self):
        modified_user = self.usr_mng.get_user('sam')
        self.usr_mng.edit_user(modified_user.get_id(), "password", False)
        modified_user = self.usr_mng.get_user('sam')
        self.assertTrue(modified_user.get('password') == "password")


if __name__ == '__main__':
    unittest.main()
