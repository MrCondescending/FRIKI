import unittest
import user
from datetime import datetime


class TestGetAllUsers(unittest.TestCase):
    def setUp(self):
        self.usr_mngr = user.UserManager("")

    def test_all_users_exist(self):
        self.assertTrue(self.usr_mngr.get_all_users(), 2)

    def test_get_last_active(self):
        self.assertTrue(self.usr_mngr.get_user("sam").get("last_active"), "15:07PM 11/21/19")

    def test_update_last_active(self):
        test_user = self.usr_mngr.get_user("name")
        current_datetime = datetime.now().strftime("%H:%M%p %m/%d/%y")
        test_user.set("last_active", current_datetime)
        self.assertTrue(test_user.get("last_active"), current_datetime)

    def test_update_last_active(self):
        test_user = self.usr_mngr.get_user("name")
        current_datetime = datetime.now().strftime("%H:%M%p %m/%d/%y")
        test_user.set("last_active", current_datetime)
        self.assertTrue(test_user.get("last_active"), current_datetime)

if __name__ == '__main__':
    unittest.main()
