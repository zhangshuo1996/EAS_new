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
