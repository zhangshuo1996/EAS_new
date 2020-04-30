"""
author:zs
date:2020-02-28
主要用于PaperSearchService类， 封装了与数据库之间的交互SQL语句
"""
import web.utils.db as db


class PaperDAO():

    teacher_paper = []

    def __init__(self, paper_id_list):
        """
        初始化数据库连接池
        """
        self.get_teacher_paper(paper_id_list)

    def return_teacher_paper(self):
        """

        :return:
        """
        return self.teacher_paper

    def get_teacher_paper(self, paper_id_list):
        """
        根据获取的论文id得到对应的教师id
        :return:[(teacher_id, paper_id), ...]
        TODO：
        """
        print("-------------------------------------get_teacher_paper----------------------------------")
        sql = "select teacher_id, paper_id from teacher_paper where paper_id in ("
        teacher_paper = []
        if len(paper_id_list) != 0:
            for paper_id in paper_id_list:
                sql += str(paper_id) + ","
            sql = sql[0:-1]
            sql += ")"
            teacher_paper = db.execute(sql)
        print(teacher_paper)
        self.teacher_paper = teacher_paper
        return teacher_paper

    def get_teacher_basic_info(self):
        """
        根据教师的多个id  (id1, id2, ...)
        获取教师的基本信息
        :return: {teacher_id1: {"school": school,
                        "institution": institution,
                        "school_id": school_id,
                        "institution_id": institution_id,
                        "name": name,
                        "title": title
                        },
                 id2: {..
                        }
                    ...
                }
        """
        print("-------------------------------------get_teacher_basic_info----------------------------------")
        teacher_paper = self.teacher_paper
        sql = "SELECT es_teacher.ID teacher_id, es_school.`NAME` school, es_institution.`NAME` institution, " \
              "es_teacher.`NAME` name, es_teacher.TITLE title, " \
              " es_teacher.SCHOOL_ID school_id, es_teacher.INSTITUTION_ID institution_id" \
              " FROM es_teacher, es_school, es_institution " \
              " where es_teacher.SCHOOL_ID = es_school.ID " \
              " and es_teacher.INSTITUTION_ID = es_institution.ID " \
              "and es_teacher.ID in ("

        for d in teacher_paper:
            teacher_id = d["teacher_id"]
            sql += str(teacher_id) + ","
        sql = sql[0:-1]
        sql += ")"
        res = db.execute(sql)
        teacher_basic_info = {}
        print(res)
        for d in res:
            tmp_dict = {
                "school": d["school"],
                "institution": d["institution"],
                "name": d["name"],
                "school_id": d["school_id"],
                "institution_id": d["institution_id"],
                "title": d["title"]
            }
            teacher_basic_info[d["teacher_id"]] = tmp_dict
        print(teacher_basic_info)
        return teacher_basic_info

    def get_institution_teacher(self):
        """
            获得成果对应的teacher以及institution
        :return: [(institution_id, teacher_id), ...]
        """
        print("-------------------------------------get_teacher_institution----------------------------------")
        teacher_paper = self.teacher_paper
        teacher_id_list = []
        for d in teacher_paper:
            teacher_id = d["teacher_id"]
            if teacher_id not in teacher_id_list:
                teacher_id_list.append(teacher_id)
        sql = "SELECT INSTITUTION_ID, ID from es_teacher where ID in ("
        for teacher_id in teacher_id_list:
            sql += str(teacher_id) + ","
        sql = sql[0: -1]
        sql += ")"
        res = db.execute(sql)
        print("res:  ", res)
        return list(res)


if __name__ == '__main__':
    paperDao = PaperDAO([73927, 73928, 73929])

    # paperDao.get_teacher_paper()
    paperDao.get_teacher_basic_info()
    paperDao.get_institution_teacher()