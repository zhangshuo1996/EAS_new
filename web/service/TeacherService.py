# """
# 获取专家基本信息以及成果信息
# """
# from web.utils import db
# import sys
# import pprint
# sys.path.append("..")
# from web.dao.TeacherDAO import *
#
#
# def get_info(teacher_id):
#     """
#
#     :param teacher_id:
#     :return:
#     """
#     teacher_info, paper_info, patent_info = get_teacher_info(teacher_id)
#     teacher_info["papers"] = paper_info
#
#     for d in patent_info:
#         d["inventor"] = eval(d["inventor"])
#         d["applicant"] = eval(d["applicant"])
#
#     teacher_info["patents"] = patent_info
#     # print(pprint.pformat(teacher_info))
#     return teacher_info