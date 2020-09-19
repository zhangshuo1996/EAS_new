"""
画像部分
"""
import os
from flask import Blueprint, current_app
from flask import render_template, request, send_from_directory
from web.service import RelationshipService as relationService
from web.log.Log import Logger
from web.service import profile as profile_service

log = Logger('log/logs/log_search', level='debug')

profile_bp = Blueprint("profile", __name__)


@profile_bp.route("/school_card")
def school_card():
    """
    展示学校卡片
    :return:
    """
    schools = ["东南大学", "浙江大学", "清华大学", "吉林大学", "武汉大学", "同济大学", "重庆大学"]
    return render_template("school_card.html", schools=schools)


@profile_bp.route("/<school>")
def index(school):
    """
    画像展示界面
    :return:
    """
    # school = "北京大学"
    labs = profile_service.get_school_lab(school=school)
    disciplines = profile_service.get_school_discipline(school)
    introduction = profile_service.get_school_introduction(school)
    return render_template("profile.html", school=school, labs=labs, disciplines=disciplines, introduction=introduction)


@profile_bp.route("/picture/<school>")
def picture(school):
    """
    展示学校图片
    """
    school_path = current_app.config["SCHOOL_PICTURE_PATH"]
    picture_path = os.path.join(school_path, school)
    pictures = os.listdir(picture_path)
    return send_from_directory(picture_path, pictures[1])


@profile_bp.route("/school_header_logo/<school>")
def school_header_logo(school):
    """
    展示学校画像中最上方的图片
    """
    path = current_app.config["SCHOOL_HEADER_PATH"]
    # avatar_path = current_app.config["SCHOOL_AVATAR_PATH"]
    avatar_path = current_app.config["BW_SCHOOL_AVATAR_PATH"]
    return profile_service.get_school_header_logo(school, path, avatar_path)


@profile_bp.route("/school_header_background/<school>")
def school_header_background(school):
    """
    展示学校画像中最上方的图片
    """
    school_path = current_app.config["SCHOOL_HEADER_PATH"]
    return profile_service.get_school_header_background(school, path=school_path)


@profile_bp.route("/get_institution_patent_num")
def get_institution_patent_num():
    """
    获取某一学校各学院的专利数量
    :return:
    """
    school = request.args.get("school")
    result = profile_service.get_institution_patent_num(school)
    return result


@profile_bp.route("/institution_profile/<school>/<institution>")
def institution_profile(school, institution):
    """
    展示学院内的画像，包括学院内部的社交关系 以及 学院内部的各项指标评估
    :return:
    """
    # school = request.args.get("school")
    # institution = request.args.get("institution")

    return render_template("institution.html", school=school, institution=institution)


@profile_bp.route("/get_institution_relation")
def get_institution_relation():
    """
    获取学院内部的社交关系
    :return:
    """
    school = request.args.get("school")
    institution = request.args.get("institution")
    teacher_ids = profile_service.get_institution_teacher_ids(school, institution)
    team_id_list = relationService.get_team_id_list_by_teacher_ids(teacher_ids)
    result = relationService.get_institution_cooperate_rel_by_team_id_list(team_id_list, institution)
    return result


@profile_bp.route("/get_institution_dimension_info")
def get_institution_dimension_info():
    """
    获取学院内部的各项指标评估
    :return:
    """
    school = request.args.get("school")
    institution = request.args.get("institution")
    result2 = profile_service.get_institution_dimension_info(school, institution)
    return result2


@profile_bp.route("/get_team_dimension_info")
def get_team_dimension_info():
    """
    获取团队的各维度信息
    :return:
    """
    team_id = request.args.get("team_id")  # team_id与教师id是对应的
    school = request.args.get("school")
    teacher_name = profile_service.get_teacher_name_by_id(team_id)
    result = profile_service.get_team_dimension_info(team_id, school)
    result["leader"] = teacher_name
    return result


@profile_bp.route('/get_school_normalize_dimension_score')
def get_school_normalize_dimension_score():
    """
    获取学校归一化之后的各维度分数
    :return:
    """
    school = request.args.get("school")
    result = profile_service.get_school_normalize_dimension_score(school)
    return result


@profile_bp.route("/update_node_visit_status")
def update_node_visit_status():
    """
    更新节点的拜访状态：0未联系过、1联系过、2做过活动、3签过合同、4创业
    :return:
    """
    teacher_id = request.args.get("teacher_id")
    visit_status = request.args.get("visit_status")
    relationService.update_node_visit_status(teacher_id, visit_status)
    return {"success": True}


# TODO： 测试词云代码
@profile_bp.route('/word_cloud')
def word_cloud():
    """
    测试词云
    :return:
    """
    return render_template("word_cloud.html")


@profile_bp.route('/page_to_pdf')
def page_to_pdf():
    """
    测试词云
    :return:
    """
    return render_template("page_to_pdf.html")

