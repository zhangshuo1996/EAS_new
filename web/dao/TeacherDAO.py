# """
# 根据教师id获取教师的基本信息以及成果信息
# 2020.3.6
# by zhang
# """
# from web.utils import db
#
#
# def get_teacher_info(teacher_id):
#     """
#
#     :param teacher_id:
#     :return:
#     """
#     # 查询基本信息
#     sql1 = "SELECT ID id, `NAME` name, TITLE title, EDUEXP edu_exp, EMAIL email, HOMEPAGE homepage, BIRTHYEAR birthyear " \
#            "from es_teacher where ID = " + str(teacher_id)
#     teacher_info = db.execute(sql1)
#     if len(teacher_info) > 0:
#         teacher_info = teacher_info[0]
#
#     sql4 = "SELECT `NAME` school_name from es_school " \
#             "where ID = (SELECT SCHOOL_ID from es_teacher where ID = " + str(teacher_id) + ")"
#     school = db.execute(sql4)[0]["school_name"]
#
#     sql5 = "SELECT `NAME` institution_name from es_institution " \
#             "where ID = (SELECT INSTITUTION_ID from es_teacher where ID = " + str(teacher_id) + ")"
#     institution = db.execute(sql5)[0]["institution_name"]
#
#     # 查询论文
#     sql2 = "SELECT id, name paper_name, org, `year`, cited_num " \
#             "from paper " \
#             "where id in ( SELECT paper_id from teacher_paper where teacher_id = " + str(teacher_id) + ")"
#     paper_info = db.execute(sql2)
#
#     # 查询专利信息
#     sql3 = "SELECT id, title, publication_year year, applicant, inventor " \
#             "from patent " \
#             "where id in ( SELECT patent_id from teacher_patent2 where teacher_id = " + str(teacher_id) + ")"
#     patent_info = db.execute(sql3)
#
#     teacher_info["school"] = school
#     teacher_info["institution"] = institution
#
#     return teacher_info, paper_info, patent_info