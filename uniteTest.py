import unittest
import novel_distributor as n

class Extract_dialog_from_file_TEST(unittest.TestCase):
    print(n.extract_dialog_from_file(r"C:\Users\Shusaku SAHASHI\PycharmProjects\norvel_distribute\novels\SF 00.txt"))

class Fitch_novel_list(unittest.TestCase):
    user = n.User()
    print(user.userID)




if __name__ == '__main__':
    unittest.main()