from flask import Blueprint, current_app, g
from flask import render_template, request, send_from_directory, render_template_string, session
from web.service.PatentSearchService import PatentSearchService
from web.service.SchoolService import SchoolService
from web.service import RelationshipService as relationService
from web.service import searchService
from web.service import profile as profile_service
from web.log.Log import Logger
from web.utils import make_pdf
import time

log = Logger('log/logs/log_search', level='debug')

search_bp = Blueprint("search", __name__)


@search_bp.route('/')
def index():
    return render_template('base.html')


@search_bp.route("/test")
def test():
    return render_template("search_outcome.html")


@search_bp.route('/hunt', methods=["GET", "POST"])
def hunt():
    """
    搜索路由
    获取要搜索的类型以及输入的内容， 根据搜索类型调用相应的SearchService
    :return:
    """
    input_key = request.form.get("input_key")
    school = request.form.get("school")
    if input_key is not None:
        start = time.time()
        patent_service = PatentSearchService(input_key, school)  # 搜索专利服务
        outcome_patent_dict = patent_service.construct_teacher_in_res()  # 获取相似成果对应的团队
        current_app.outcome = outcome_patent_dict
        outcome_id = searchService.save_this_search_text(1, input_key)  # 记录该次搜索的企业需求
        search_history = patent_service.get_search_history()
        end = time.time()
        spend_time = end - start
        print("搜索时间", spend_time, "秒")
        return render_template("search_outcome.html", input_key=input_key, outcome_paper_list=[], outcome_id=outcome_id,
                               data=outcome_patent_dict, type="teacher", search_history=search_history, school=school)
    else:
        return render_template('search.html')


# @search_bp.route("/get_search_outcome")
# def get_search_outcome():
#     """
#     根据搜索的关键字获取搜索结果， ajax专用
#     :return:
#     """
#     input_key = request.args.get("input_key")
#     patent_service = PatentSearchService(input_key)  # 搜索专利服务
#     outcome_patent_list = patent_service.construct_teacher_in_res()
#     return {"data": outcome_patent_list}


@search_bp.route('/school_profile/<school>')
def school_profile(school):
    """
    TODO: 展示学校画像
    :param school:
    :return:
    """
    school_service = SchoolService()
    try:
        introduction = school_service.get_introduction(school)
        key_discipline_list = school_service.get_key_discipline(school)
        return render_template("school.html", school=school, introduction=introduction, key_discipline_list=key_discipline_list)
    except Exception as e:
        print(e)
        print("未找到该大学")
        return render_template('error.html')


@search_bp.route('/getTeamRelation')
def getTeamRelation():
    """
    获取该团队的关系数据
    :return:
    """
    team_id = request.args.get("team_id")
    institution = request.args.get("institution")
    result = relationService.get_cooperate_rel_by_team_id_list([team_id], institution)
    teacher_name = profile_service.get_teacher_name_by_id(team_id)
    result["leader"] = teacher_name
    return result


@search_bp.route("/avatar/<filename>")
def avatar(filename):
    """
    寻找头像
    """
    # upload_path = current_app.config["SCHOOL_AVATAR_PATH"]
    avatar_path = current_app.config["BW_SCHOOL_AVATAR_PATH"]
    return send_from_directory(avatar_path, filename + '.png')


@search_bp.route("/get_pdf", methods=["POST"])
def get_pdf3():
    """
    获取搜索结果中 第i个 团队对应的pdf
    :return:
    """
    page_num = request.form.get("page_num")
    outcome = current_app.outcome
    doc_path, filename = make_pdf.do_test(page_num, outcome)
    return send_from_directory(doc_path, filename)


