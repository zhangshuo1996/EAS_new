from flask import Blueprint, current_app
from flask import render_template, request, send_from_directory
from web.service.PatentSearchService import PatentSearchService
from web.service.SchoolService import SchoolService
from web.service import RelationshipService as relationService
from web.service import searchService
from web.log.Log import Logger
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
        # try:
        start = time.time()
        # 记录该次搜索的企业需求
        searchService.save_this_search_text(1, input_key)
        patent_service = PatentSearchService(input_key, school)  # 搜索专利服务
        outcome_patent_dict = patent_service.construct_teacher_in_res()  # 获取相似成果对应的团队
        search_history = patent_service.get_search_history()
        end = time.time()
        spend_time = end - start
        print("搜索时间", spend_time, "秒")
        return render_template("search_outcome.html", input_key=input_key, outcome_paper_list=[],
                               data=outcome_patent_dict, type="teacher", search_history=search_history, school=school)
        # except Exception as e:
        #     return render_template('error.html')
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


@search_bp.route('/getInstitutionRelation')
def getInstitutionRelation():
    """
    获取该团队的关系数据
    :return:
    """
    team_id = request.args.get("team_id")
    institution = request.args.get("institution")
    result = relationService.get_cooperate_rel_by_team_id_list([team_id], institution)
    return result

# 待删除
# @search_bp.route('/institution/<school>/<institution>', methods=["GET"])
# def institution(school, institution):
#     print(school, institution)
#     try:
#         institution_service = InstitutionService()
#         outcome_list, discipline = institution_service.get_institution_patent(school, institution)
#         ip = request.remote_addr
#         log.logger.info(log.combine_msg(ip=ip, username="none", event="visit_institution_page",
#                                         message="normal|" + school + institution))
#         if outcome_list is None or discipline is None:
#             return render_template("error.html")
#         else:
#             return render_template("institution.html", outcome_list=outcome_list, discipline=discipline)
#
#     except Exception as e:
#         print("输入的学校或学院有误", e)
#         ip = request.remote_addr
#         log.logger.warn(log.combine_msg(ip=ip, username="none", event="visit_institution_page",
#                                         message="warn|" + school + institution + "|" + traceback.format_exc()))
#         return render_template("error.html")


# 待删除
# @search_bp.route('/teacher/<teacher_id>', methods=["GET"])
# def teacher(teacher_id):
#     """
#     :param teacher_id:
#     :return:
#     """
#     print(teacher_id)
#     teacher_net = get_teacher_net(teacher_id)
#     teacher_info = get_info(teacher_id)
#     print(teacher_net)
#     print(teacher_info)
#     return render_template("teacher.html", teacher_net=teacher_net, teacher=teacher_info)


@search_bp.route("/avatar/<filename>")
def avatar(filename):
    """
    寻找头像
    """
    # upload_path = current_app.config["SCHOOL_AVATAR_PATH"]
    avatar_path = current_app.config["BW_SCHOOL_AVATAR_PATH"]
    return send_from_directory(avatar_path, filename + '.png')
