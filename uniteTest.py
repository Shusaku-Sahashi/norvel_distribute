import unittest
import novel_distributor as n

# class Extract_dialog_from_file_TEST(unittest.TestCase):
#     for i in n.extract_dialog_from_file("SF 00.txt"):
#         print(i)

class Fitch_novel_list(unittest.TestCase):

    def test_user(self):
        novel_list = n.fitch_novel_list()
        novel_title = novel_list[0]
        novel = n.extract_dialog_from_file(novel_title)
        user = n.User(novel_title=novel_title, novel=novel)

        self.assertEqual(user.novel_title, novel_title)
        self.assertEqual(len(user.userID), 10)

    def test_pkl(self):
        print(__name__)
        novel_list = n.fitch_novel_list()
        novel_title = novel_list[0]
        novel = n.extract_dialog_from_file(novel_title)
        user = n.User(novel_title=novel_title, novel=novel)

        n.persist_pkl(user)

        user_2 = n.load_pkl(user.userID)

        self.assertEqual(user.userID, user_2.userID)

if __name__ == '__main__':
    unittest.main()