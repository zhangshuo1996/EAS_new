from web.utils import db


class PatentDAO():

    teacher_patent = []

    def __init__(self, patent_id_list, school):
        """

        """
        self.get_teacher_patent(patent_id_list, school)

    def return_teacher_patent(self):
        """
        :return:
        """
        return self.teacher_patent

    def get_teacher_patent(self, patent_id_list, school):
        """
        根据获取的专利id得到对应的教师id,以及专利名
        :return:
            [
                {
                    "teacher_id": 11,
                    "patent_id": 11,
                    "patent_name":
                }
            ]
        """
        sql = """
            select i.id teacher_id, i.name teacher_name, p.id patent_id, p.title patent_name, s.id school_id, s.name school_name
            from clean_inventor_backup i
            LEFT JOIN c_inventor_patent_backup ip
            on i.id = ip.inventor_id
            LEFT JOIN patent p
            on ip.patent_id = p.id
            LEFT JOIN school s
            on i.school_id = s.id
            where s.name = \"{school}\" and p.id in (
        """.format(school=school)
        # 上面sql中的s.name = school 条件用于只取某一学校的成果
        teacher_patent = []
        # sql = "("
        if len(patent_id_list) != 0:
            for patent_id in patent_id_list:
                sql += str(patent_id) + ","
            sql = sql[0:-1]
            sql += ")"
            print(sql)
            teacher_patent = db.select(sql)
        self.teacher_patent = teacher_patent

    def get_teacher_basic_info(self):
        """
        根据教师的多个id  (id1, id2, ...)
        获取教师的基本信息
        :return: {id1: {"school": school,
                        "institution": institution,
                        "school_id": school_id,
                        "institution_id": institution_id,
                        "lab": lab,
                        "name": name,
                        "title": title
                        },
                 id2: {..
                        }
                    ...
                }
        """
        print("-------------------------------------get_teacher_basic_info----------------------------------")
        teacher_patent = self.teacher_patent
        sql = """
            select i.id teacher_id, i.name  name, s.name school, s.id school_id, i.lab,
            i.institution institution, "教授" title, 111 institution_id
            from clean_inventor_backup i
            LEFT JOIN school s
            on i.school_id = s.id
            where i.id in (
        """
        for d in teacher_patent:
            teacher_id = d["teacher_id"]
            sql += str(teacher_id) + ","
        sql = sql[0:-1]
        sql += ")"
        res = db.select(sql)
        teacher_basic_info = {}
        for d in list(res):
            tmp_dict = {
                "school": d["school"],
                "lab": d["lab"],
                "institution": d["institution"],
                "name": d["name"],
                "school_id": d["school_id"],
                "institution_id": d["institution_id"],
                "title": d["title"]
            }
            teacher_basic_info[d["teacher_id"]] = tmp_dict
        print(teacher_basic_info)
        return teacher_basic_info

    def get_teacher_project_info(self):
        """
        获取该专家对应的项目信息
        :return: [{"teacher_id": **, "project_name": **}]
        """
        sql = """
            select p.teacher_id, p.name project_name
            from project p
            where p.teacher_id in (
        """
        for d in self.teacher_patent:
            teacher_id = d["teacher_id"]
            sql += str(teacher_id) + ","
        sql = sql[0:-1]
        sql += ")"
        result = db.select(sql)
        return result

    def get_search_history(self):
        """
        获取历史搜索记录
        :return:
        """
        sql = """
            select search_text, gmt_create
            from search_history
            limit 5
        """
        return db.select(sql)


if __name__ == '__main__':
    patentDao = PatentDAO([1432982])
