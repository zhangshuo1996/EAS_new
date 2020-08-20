import unittest
from web.dao.PatentDAO import *
from web.utils import db
from web.config import *


class TestGetTeacherPatent(unittest.TestCase):
    """

    """

    def setUp(self) -> None:
        db.create_engine(**DB_CONFIG)

    def tearDown(self) -> None:
        pass

    def test_1(self):
        """

        :return:
        """
        patentDao = PatentDAO([472887, 472918, 473205, 473250, 473286])


    def test_delete_list(self):
        """
        测试 边循环 边删除列表
        :return:
        """
        a = [1, 4, 3, 2, 6, 8, 11, 10]
        for l in a[::-1]:
            print("--", l)
            if l % 2 == 0:
                a.remove(l)
        print(a)
