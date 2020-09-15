from web.dao import profile as profile_dao
from web.service import RelationshipService as relationService
from flask import send_from_directory
import math
import os


def get_school_header_logo(school, path, avatar_path):
    """
    展示学校画像中最上方的图片中的学校图标
    """
    file_names = os.listdir(path)
    pic_file_name = ""
    for file_name in file_names:
        if school in file_name and "logo" in file_name:
            pic_file_name = file_name
            break
    if pic_file_name == "":
        pic_file_name = school + ".png"
        return send_from_directory(avatar_path, pic_file_name)
    else:
        return send_from_directory(path, pic_file_name)


def get_school_header_background(school, path):
    """
    展示学校画像中最上方图片中的背景
    """
    file_names = os.listdir(path)
    pic_file_name = "default_pic.png"
    for file_name in file_names:
        if school in file_name and "logo" not in file_name:
            pic_file_name = file_name
            break
    return send_from_directory(path, pic_file_name)


def get_school_discipline(school):
    """
    获取学校的重点学科
    :param school:
    :return:
    """
    _data = profile_dao.get_school_discipline(school)
    return _data


def get_school_introduction(school):
    """
    获取学校的简介
    :param school:
    :return:
    """
    result = profile_dao.get_school_introduction(school)
    return result["introduction"]


def get_school_lab(school):
    """
    获取学院的实验平台
    :param school:
    :return:
    """
    _data = profile_dao.get_school_lab(school)
    result = []
    for dic in _data:
        if "国家" in dic["lab"] or "省" in dic["lab"]:
            result.append(dic)
    return result


def get_institution_patent_num(school):
    """
    获取某一学校各学院的专利数量
    :return:
    """
    _data = profile_dao.get_institution_patent_num(school)
    institutions = []
    series = []
    for dic in _data:
        institutions.append(dic["institution"])
        series.append(dic["cnt"])

    return {
        "institutions": institutions,
        "series": series
    }


# def get_team_info(school, institution):
#     """
#     获取这个学院下的团队信息
#     :param school:
#     :param institution:
#     :return:
#     """
#     # 1. 获取这个学院下的所有人 id
#     teacher_ids = profile_dao.get_institution_teacher_id(school, institution)
#     teacher_id_list = [dic["teacher_id"] for dic in teacher_ids]
#     # 2. 获取这些人对应的团队id
#     team_id_list = get_team_ids_by_teacher_ids(teacher_id_list)
#     # 3. 获取这些团队的信息，包括主要成员以及其他成员


def get_institution_teacher_ids(school, institution):
    """
    获取该学校该学院下的老师id
    :param school:
    :param institution:
    :return:
    """
    _data = profile_dao.get_institution_teacher_id(school, institution)
    teacher_ids = [dic["teacher_id"] for dic in _data]
    return teacher_ids


def get_teacher_name_by_id(team_id):
    """

    :param team_id:
    :return:
    """
    result = profile_dao.get_teacher_name_by_id(team_id)
    return result["name"]


def get_team_dimension_info(team_id, school):
    """
    获取团队的各维度信息
    :return:
    """
    # 1. 根据团队id获取该团队的所有成员id
    teacher_ids = relationService.get_teacher_team(teacher_id=team_id)
    # 2. 根据成员id获取这些成员中的头衔信息，专利数量，项目数量，所在的实验室列表
    dimension_info = get_teachers_info(list(teacher_ids), school)
    researcher_num = len(list(teacher_ids))
    # 3. 根据获取的各维度信息进行综合打分
    school_level_score = cal_school_score_by_discipline(dimension_info["good_discipline_num"])
    achieve_num = cal_achieve_score(dimension_info["patent_num"])
    researcher_num_score = cal_researcher_num_score(researcher_num)
    researcher_level_score = cal_researcher_level_score(dimension_info["academician_num"], dimension_info["excellent_young"])
    lab_score = cal_lab_score(dimension_info["national_lab_num"], dimension_info["province_lab_num"])
    project_score = cal_project_num_score(dimension_info["project_num"])
    return {
        "school_level_score":  school_level_score,
        "achieve_num": achieve_num,
        "researcher_num_score":  researcher_num_score,
        "researcher_level_score":  researcher_level_score,
        "lab_score":  lab_score,
        "project_score": project_score
    }


def get_teachers_info(teacher_ids, school):
    """
    根据多个教师的id获取这些教师的基本信息、学校信息、成果信息
    :param school:
    :param teacher_ids:
    :return:
    """
    # 1. 获取教师的实验平台信息， 荣誉信息（院士，长江...)
    lab_honor_info = profile_dao.get_labs_honors_by_teacher_ids(teacher_ids)
    academician_num, excellent_young, national_lab_num, province_lab_num = statistic_lab_honor_info(lab_honor_info)
    # 2. 获取多个教师的的拥有的专利数量
    patents = profile_dao.get_patent_num_by_teacher_ids(teacher_ids)
    patent_num = len(patents)
    # 3. 获取这些学校的一流学科数量，证明其学校水平
    discipline = profile_dao.get_good_discipline_num_by_school(school)
    discipline_num = discipline[0]["cnt"]
    # 4. 获取这一团队的项目数量
    project_num = profile_dao.get_project_num_by_teacher_ids(teacher_ids)["cnt"]
    dimensions_info = {
        "academician_num": academician_num,  # 院士数量
        "excellent_young": excellent_young,  # 长江、杰青数量
        "national_lab_num": national_lab_num,  # 是否有国家、教育部重点实验室
        "province_lab_num": province_lab_num,  # 是否有省级重点实验室
        "patent_num": patent_num,  # 专利数量
        "good_discipline_num": discipline_num,  # 该学校的一流学科数量
        "project_num": project_num
    }
    return dimensions_info


def statistic_lab_honor_info(lab_honor_info):
    """
    根据一个学校中所有教师的荣誉与实验室信息，统计该学校下的荣誉与实验室信息
    :param lab_honor_info:
    :return:
    """
    academician_num = 0
    excellent_young = 0
    national_lab_num = 0
    province_lab_num = 0
    for dic in lab_honor_info:
        lab = dic["lab"] if dic["lab"] is not None else ""
        honor = dic["honor"] if dic["honor"] is not None else ""
        if "国家" in lab or "教育部" in lab:
            national_lab_num += 1
        if "省" in lab:
            province_lab_num += 1

        if "长江" in honor or "杰青" in honor:
            excellent_young += 1
        if "院士" in honor:
            academician_num += 1

    return academician_num, excellent_young, national_lab_num, province_lab_num


def get_school_normalize_dimension_score(school):
    """
    获取学校归一化之后的各维度分数
    TODO: 评分指标待调整，目前使用的评分是对团队各项指标的评分标准
    :return:
    """
    # 1. 获取学校中所有教师的头衔信息，专利数量，项目数量，所在的实验室列表
    dimension_info = get_school_dimensions_info(school)
    # 2. 根据获取的各维度信息进行综合打分
    school_level_score = cal_school_score_by_discipline(dimension_info["good_discipline_num"])
    achieve_num = cal_achieve_score(dimension_info["patent_num"])
    researcher_num_score = cal_researcher_num_score(dimension_info["researcher_num"])
    researcher_level_score = cal_researcher_level_score(dimension_info["academician_num"], dimension_info["excellent_young"])
    lab_score = cal_lab_score(dimension_info["national_lab_num"], dimension_info["province_lab_num"])
    return {
        "school_level_score":  school_level_score,
        "achieve_num": achieve_num,
        "researcher_num_score":  researcher_num_score,
        "researcher_level_score":  researcher_level_score,
        "lab_score":  lab_score,
    }


def get_school_dimensions_info(school):
    """
    获取该学校的各维度信息
    :param school:
    :return: {
                "academician_num": academician_num,    # 院士数量
                "excellent_young": excellent_young,    # 杰青数量
                "national_lab_num": national_lab_num,  # 国家、教育部重点实验室数量
                "patent_num": patent_num,              # 专利数量
                "good_discipline_num": discipline_num, # 该学校的一流学科数量
            }
    """
    # 获取该学校下教师的荣誉与实验室信息
    lab_honor_info = profile_dao.get_school_teacher_info(school)
    academician_num, excellent_young, national_lab_num, province_lab_num = statistic_lab_honor_info(lab_honor_info)
    # 获取该学校下教师的专利数量
    patent_num = profile_dao.get_school_teacher_patent_num(school)["cnt"]
    # 获取这些学校的一流学科数量，证明其学校水平
    discipline = profile_dao.get_good_discipline_num_by_school(school)
    discipline_num = discipline[0]["cnt"]
    # 获取该学校的研究人员数量
    researcher_num = profile_dao.get_school_teacher_num(school)["cnt"]
    dimensions_info = {
        "academician_num": academician_num,  # 院士数量
        "excellent_young": excellent_young,  # 长江、杰青数量
        "national_lab_num": national_lab_num,  # 是否有国家、教育部重点实验室
        "province_lab_num": province_lab_num,  # 是否有省级重点实验室
        "patent_num": patent_num,  # 专利数量
        "good_discipline_num": discipline_num,  # 该学校的一流学科数量
        "researcher_num": researcher_num,  # 该学校研究人员数量
    }
    return dimensions_info


def cal_school_score_by_discipline(discipline_num):
    """
    根据一流学科数量为学校水平打分
    :param discipline_num:
    :return:
    """
    if discipline_num == 0:
        return 50
    elif discipline_num <= 1:
        return 55
    elif discipline_num <= 3:
        return 60
    elif discipline_num <= 6:
        return 70
    elif discipline_num <= 10:
        return 80
    elif discipline_num <= 20:
        return 90
    else:
        return 100


def cal_achieve_score(patent_num):
    """
    计算成果数量得分
    :param patent_num:
    :return:
    """
    if patent_num > 1000:
        return 100
    elif patent_num > 800:
        return 90
    elif patent_num > 500:
        return 80
    elif patent_num > 200:
        return 70
    elif patent_num > 100:
        return 60
    return 50


def cal_researcher_num_score(researcher_nums):
    """
    计算研究人员数量得分
    :param researcher_nums:
    :return:
    """
    if researcher_nums > 50:
        return 100
    elif researcher_nums > 40:
        return 90
    elif researcher_nums > 30:
        return 80
    elif researcher_nums > 20:
        return 70
    elif researcher_nums > 10:
        return 60
    return 50


def cal_researcher_level_score(academician_num, excellent_young):
    """
    计算研究人员水平
    :param academician_num:
    :param excellent_young:
    :return:
    """
    if academician_num >= 1:
        return 100
    if excellent_young == 1:
        return 80
    if excellent_young > 1:
        return 90
    return 70


def cal_lab_score(national_lab_num, province_lab_num):
    """
    计算实验平台得分
    :param national_lab_num:
    :param province_lab_num:
    :return:
    """
    if national_lab_num >= 1:
        return 100
    if province_lab_num > 1:
        return 90
    if province_lab_num == 1:
        return 80
    return 60


def cal_project_num_score(project_num):
    """
    计算团队项目数量得分
    :param project_num:
    :return:
    """
    if project_num > 200:
        return 100
    if project_num > 150:
        return 90
    if project_num > 100:
        return 80
    if project_num > 50:
        return 70
    if project_num > 30:
        return 60
    return 50
