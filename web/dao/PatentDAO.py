from web.utils import db


class PatentDAO():

    teacher_patent = []

    def __init__(self, patent_id_list):
        """

        """
        self.get_teacher_patent(patent_id_list)

    def return_teacher_patent(self):
        """

        :return:
        """
        return self.teacher_patent

    def get_teacher_patent(self, patent_id_list):
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
        print("-------------------------------------get_teacher_patent----------------------------------")
        # sql = "select teacher_id, patent_id from teacher_patent3 where patent_id in ("
        # sql = """
        #     select tp.teacher_id teacher_id, tp.patent_id patent_id, p.title patent_name
        #     from teacher_patent3 tp left join patent3 p
        #     on tp.patent_id = p.id
        #     where patent_id in (
        # """
        sql = """
            select i.id teacher_id, i.name teacher_name, p.id patent_id, p.title patent_name, s.id school_id, s.name school_name
            from clean_inventor_backup i
            LEFT JOIN c_inventor_patent_backup ip
            on i.id = ip.inventor_id
            LEFT JOIN patent p
            on ip.patent_id = p.id
            LEFT JOIN school s
            on i.school_id = s.id
            where p.id in (
        """
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
            select i.id teacher_id, i.name  name, s.name school, s.id school_id, 
            "学院" institution, "教授" title, 111 institution_id
            from clean_inventor_backup i
            LEFT JOIN school s
            on i.school_id = s.id
            where i.id in (
        """
        # sql = "SELECT es_teacher.ID teacher_id, es_school.`NAME` school, es_institution.`NAME` institution," \
        #       " es_teacher.`NAME` name, es_teacher.TITLE title, " \
        #       " es_teacher.SCHOOL_ID school_id, es_teacher.INSTITUTION_ID institution_id" \
        #       " FROM es_teacher, es_school, es_institution " \
        #       " where es_teacher.SCHOOL_ID = es_school.ID " \
        #       " and es_teacher.INSTITUTION_ID = es_institution.ID " \
        #       "and es_teacher.ID in ("

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
                "institution": d["institution"],
                "name": d["name"],
                "school_id": d["school_id"],
                "institution_id": d["institution_id"],
                "title": d["title"]
            }
            teacher_basic_info[d["teacher_id"]] = tmp_dict
        print(teacher_basic_info)
        return teacher_basic_info


if __name__ == '__main__':
    patentDao = PatentDAO([1432982])
