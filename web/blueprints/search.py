from flask import Blueprint, current_app
from flask import render_template, request, send_from_directory
from web.service.PatentSearchService import PatentSearchService
from web.service.InstitutionService import InstitutionService
from web.service.SchoolService import SchoolService
from web.service.RelationshipService import *
from web.service.TeacherService import *
from web.service import searchService
import traceback
from web.log.Log import Logger

log = Logger('log/logs/log_search', level='debug')

search_bp = Blueprint("search", __name__)


@search_bp.route('/')
def index():
    return render_template('base.html')


@search_bp.route("/test")
def test():
    return render_template("test.html")


@search_bp.route('/hunt', methods=["GET", "POST"])
def hunt():
    """
    搜索路由
    获取要搜索的类型以及输入的内容， 根据搜索类型调用相应的SearchService
    :return:
    """
    input_key = request.form.get("input_key")
    if input_key is not None:
        try:
            # 记录该次搜索的企业需求
            searchService.save_this_search_text(1, input_key)
            patent_service = PatentSearchService(input_key)  # 搜索专利服务
            outcome_patent_list = patent_service.construct_teacher_in_res()
            return render_template("search_outcome.html", input_key=input_key, outcome_paper_list=[], outcome_patent_list=outcome_patent_list, type="teacher")
        except Exception:
            return render_template('error.html')
    else:
        return render_template('search.html')


@search_bp.route("/get_search_outcome")
def get_search_outcome():
    """
    根据搜索的关键字获取搜索结果， ajax专用
    :return:
    """
    input_key = request.args.get("input_key")
    patent_service = PatentSearchService(input_key)  # 搜索专利服务
    outcome_patent_list = patent_service.construct_teacher_in_res()
    return {"data": outcome_patent_list}


@search_bp.route('/school/<school>')
def school(school):
    school_service = SchoolService()
    try:
        introduction = school_service.get_introduction(school)
        key_discipline_list = school_service.get_key_discipline(school)
        return render_template("school.html", school=school, introduction=introduction, key_discipline_list=key_discipline_list)
    except Exception as e:
        print(e)
        print("未找到该大学")
        return render_template('error.html')


@search_bp.route('/institution/<school>/<institution>', methods=["GET"])
def institution(school, institution):
    print(school, institution)
    try:
        institution_service = InstitutionService()
        outcome_list, discipline = institution_service.get_institution_patent(school, institution)
        ip = request.remote_addr
        log.logger.info(log.combine_msg(ip=ip, username="none", event="visit_institution_page",
                                        message="normal|" + school + institution))
        if outcome_list is None or discipline is None:
            return render_template("error.html")
        else:
            return render_template("institution.html", outcome_list=outcome_list, discipline=discipline)

    except Exception as e:
        print("输入的学校或学院有误", e)
        ip = request.remote_addr
        log.logger.warn(log.combine_msg(ip=ip, username="none", event="visit_institution_page",
                                        message="warn|" + school + institution + "|" + traceback.format_exc()))
        return render_template("error.html")


@search_bp.route('/teacher/<teacher_id>', methods=["GET"])
def teacher(teacher_id):
    """
    :param teacher_id:
    :return:
    """
    print(teacher_id)
    teacher_net = get_teacher_net(teacher_id)
    teacher_info = get_info(teacher_id)
    print(teacher_net)
    print(teacher_info)
    return render_template("teacher.html", teacher_net=teacher_net, teacher=teacher_info)


@search_bp.route("/avatar/<filename>")
def avatar(filename):
    """
    寻找头像
    """
    upload_path = current_app.config["SCHOOL_AVATAR_PATH"]
    return send_from_directory(upload_path, filename + '.png')


