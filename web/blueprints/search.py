from flask import Blueprint
from flask import Flask, render_template, request
from web.forms import InputKeyForm
from web.service.PaperSearchService import PaperSearchService
from web.service.PatentSearchService import PatentSearchService
from web.service.InstitutionService import InstitutionService
from web.service.SchoolService import SchoolService
from web.service.RelationshipService import *
from web.service.TeacherService import *
import traceback
from web.log.Log import Logger

log = Logger('log/logs/log_search', level='debug')

search_bp = Blueprint("search", __name__)


@search_bp.route('/')
def index():

    ip = request.remote_addr  # 获取用户ip
    # log.logger.debug(log.combine_msg(ip=ip, username="none", event="visit_start_page", message="normal"))
    return render_template('base.html')


@search_bp.route('/hunt', methods=["GET", "POST"])
def hunt():
    """
    搜索路由
    获取要搜索的类型以及输入的内容， 根据搜索类型调用相应的SearchService
    :return:
    """
    form = InputKeyForm()
    input_key = request.form.get('input_key')  # 输入的内容
    # select_type = request.form.get('select_type')  # 搜索的类型
    select_type = "搜索专家"
    if input_key is not None:
        try:
            paperService = PaperSearchService(input_key)  # 搜索论文服务
            patentService = PatentSearchService(input_key)  # 搜索专利服务
            if select_type == "搜索专家":
                outcome_paper_list = paperService.construct_teacher_in_res()
                outcome_patent_list = patentService.construct_teacher_in_res()
                ip = request.remote_addr
                # log.logger.info(log.combine_msg(ip=ip, username="none", event="visit_search_page",
                #                                 message="normal|" + select_type + "|" + input_key))
                return render_template("search_outcome.html", input_key=input_key,
                                       outcome_paper_list=outcome_paper_list, outcome_patent_list=outcome_patent_list, type="teacher")
            else:
                outcome_paper_list = paperService.construct_institution_info()
                outcome_patent_list = patentService.construct_institution_info()
                ip = request.remote_addr
                # log.logger.info(log.combine_msg(ip=ip, username="none", event="visit_search_page",
                #                                 message="normal|" + select_type + "|" + input_key))
                return render_template("search_outcome.html", outcome_paper_list=outcome_paper_list, outcome_patent_list=outcome_patent_list, type="institution")

        except Exception as e:
            ip = request.remote_addr
            # log.logger.error(log.combine_msg(ip=ip, username="none", event="visit_search_page", message="error|" + select_type + "|" + input_key + "|" + traceback.format_exc()))
            # print("error when input key : %s" % e)
            return render_template('error.html')
    else:
        ip = request.remote_addr
        # log.logger.info(log.combine_msg(ip=ip, username="none", event="visit_search_page",
        #                                 message="normal|none"))
        return render_template('search.html', form=form)


@search_bp.route('/school/<school>')
def school(school):
    schoolService = SchoolService()
    try:
        introduction = schoolService.get_introduction(school)
        key_discipline_list = schoolService.get_key_discipline(school)
        ip = request.remote_addr
        # log.logger.info(log.combine_msg(ip=ip, username="none", event="visit_school_page",
        #                                 message="normal|" + school))
        return render_template("school.html", school=school, introduction=introduction, key_discipline_list=key_discipline_list)
    except Exception as e:
        print(e)
        print("未找到该大学")
        ip = request.remote_addr
        # log.logger.warn(log.combine_msg(ip=ip, username="none", event="visit_school_page",
        #                                 message="warn|" + school + "|" + traceback.format_exc()))
        return render_template('error.html')


@search_bp.route('/institution/<school>/<institution>', methods=["GET"])
def institution(school, institution):
    print(school, institution)
    try:
        institutionService = InstitutionService()
        outcome_list, discipline = institutionService.get_institution_patent(school, institution)
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


