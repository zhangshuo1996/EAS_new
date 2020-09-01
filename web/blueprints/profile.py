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


@profile_bp.route("/")
def index():
    """
    画像展示界面
    :return:
    """
    school = "河海大学"
    labs = profile_service.get_school_lab(school=school)
    disciplines = profile_service.get_school_discipline(school)
    return render_template("profile.html", school=school, labs=labs, disciplines=disciplines)


@profile_bp.route("/picture/<school>")
def picture(school):
    """
    展示学校图片
    """
    school_path = current_app.config["SCHOOL_PICTURE_PATH"]
    picture_path = os.path.join(school_path, school)
    pictures = os.listdir(picture_path)
    return send_from_directory(picture_path, pictures[6])


@profile_bp.route("/school_header/<school>")
def school_header(school):
    """
    展示学校画像中最上方的图片
    """
    school = "东南大学"
    school_path = current_app.config["SCHOOL_HEADER_PATH"]
    return send_from_directory(school_path, school + ".png")


@profile_bp.route("/get_institution_patent_num")
def get_institution_patent_num():
    """
    获取某一学校各学院的专利数量
    :return:
    """
    school = request.args.get("school")
    result = profile_service.get_institution_patent_num(school)
    return result


@profile_bp.route("/getInstitutionRelation")
def getInstitutionRelation():
    """
    获取该学院中的关系数据
    :return:
    """
    school = request.args.get("school")
    institution = request.args.get("institution")
    teacher_ids = profile_service.get_institution_teacher_ids(school, institution)
    result = relationService.get_cooperate_rel(teacher_ids)
    return result


@profile_bp.route("/get_team_dimension_info")
def get_team_dimension_info():
    """
    获取团队的各维度信息
    :return:
    """
    team_id = request.args.get("team_id")
    school = request.args.get("school")
    result = profile_service.get_team_dimension_info(team_id, school)

    return result
