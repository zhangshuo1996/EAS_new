"""
@author: zs
@date: 2020.2.17
update: 2020.8.17-19
"""
import requests
import json
import sys
import logging
from web.dao.PatentDAO import PatentDAO
from web.service import RelationshipService

sys.path.append("..")
logger = logging.getLogger(__name__)


class PatentSearchService:
    """
    为搜索提供服务
    """
    patent_id_list = []
    distance_list = []
    id_dis_dict = {}
    teacher_patent = []
    teacher_basic_info = None
    patentDao = None
    school = None

    def __init__(self, input_key, school):
        """
        初始化service
        :param input_key:
        :param school:
        """
        self.school = school
        self.get_ids_by_input(input_key)  # 调用restful服务获得相似的专利id
        self.combine_id_distance()
        self.patentDao = PatentDAO(patent_id_list=self.patent_id_list, school=school)  # 实例化专利数据类
        self.teacher_patent = self.patentDao.return_teacher_patent()  # 获取专利与教师的对应
        self.teacher_basic_info = self.patentDao.get_teacher_basic_info()  # 获取教师的基本信息

    def get_search_history(self):
        """
        获取历史搜索记录
        :return:
        """
        result = self.patentDao.get_search_history()
        return result

    def get_patent_info(self):
        """
        获取patent_id为键， 专利名为值的字典
        :return:
        """
        patent_info = {}
        for dic in self.teacher_patent:
            patent_id = dic["patent_id"]
            patent_name = dic["patent_name"]
            patent_info[patent_id] = patent_name
        return patent_info

    def get_ids_by_input(self, input_key):
        """
        根据用户的输入内容, 通过调用restful服务获取与之相关的成果id
        :return:
        """
        data = {"K": 200, "key": input_key}
        url = "http://39.100.224.138:8777/search"
        data_json = json.dumps(data)
        headers = {'Content-type': 'application/json'}
        response = requests.post(url, data=data_json, headers=headers)
        i_string = eval(response.text)["I"]  # 返回的成果ID列表（字符串形式）
        d_string = eval(response.text)["D"]  # 返回的成果距离列表 （字符串形式）
        i_list = eval(i_string)
        d_list = eval(d_string)
        print("-----------------------------------get_ids_by_input--相似成果id获取成功-----------------------------------")
        self.patent_id_list = i_list[0]
        self.distance_list = d_list[0]

    def combine_id_distance(self):
        """
        将patent_id列表与distance列表组合成字典
        :return: {id1: dis1, id2: dis2, ...}
        """
        for i in range(len(self.patent_id_list)):
            if self.patent_id_list[i] not in self.id_dis_dict.keys():
                self.id_dis_dict[self.patent_id_list[i]] = self.distance_list[i]

    def get_this_teacher_patents(self):
        """
        获取某一个教师的专利 --> {teacher_id1: [patent_id1, patent_id2],}
        :return:
        """
        teacher_all_patent = {}
        teacher_patent = self.teacher_patent
        for d in teacher_patent:
            teacher_id = d["teacher_id"]
            patent_id = d["patent_id"]
            if teacher_id not in teacher_all_patent.keys():
                teacher_all_patent[teacher_id] = [patent_id]
            else:
                tmp_list = teacher_all_patent[teacher_id]
                tmp_list.append(patent_id)
                teacher_all_patent[teacher_id] = tmp_list
        return teacher_all_patent

    def cal_teacher_patent_dist(self, teacher_all_patent):
        """
        计算每一教师对应所有成果相似度的平均距离和最小距离
        :return:
        """
        teacher_avg_min = {}
        for teacher_id in teacher_all_patent:
            sum_dis = 0
            min_dis = 100000000
            for paper_id in teacher_all_patent[teacher_id]:
                sum_dis += self.id_dis_dict[paper_id]
                min_dis = min(min_dis, self.id_dis_dict[paper_id])
            dis_avg = sum_dis / len(teacher_all_patent[teacher_id])
            teacher_avg_min[teacher_id] = (dis_avg, min_dis)
        return teacher_avg_min

    def construct_teacher_in_res(self):
        """
        构造位于返回结果中的教师的信息
        {
            "team_list": [
                {
                    team_id1: {"team_id": **, "school": *, "institution": * "lab": *, "member_id_list": , "patent_list": *, "project_list"}
                }, ...
            ],
            "teacher_base_info":{
                teacher_id: {"lab": *, "institution": *, "school': "title": *, "name": *, "achieve_nums": *, "patent_list": *, "project_list"},
                .....
            }
            "patent_info": {
                patent_id: patent_name,
                ....
            },
            "school_proportion":{
                "legend": [school1, school2, ...],
                "series": [{"name": school1, 'value': 7}],  value 是该学校拥有的相似成果的数量
                "seriesName": "学校数量占比"
            }
        }
        :return:
        """
        print("-------------------------------------construct_teacher_in_res----------------------------------")
        # 1. find 专家对应的所有成果 --> {teacher_id1: [patent_id1, patent_id2],}
        teacher_all_patent = self.get_this_teacher_patents()

        # 2. construct 平均距离和最小距离字典teacher_avg_min --> {teacher_id: (dis_average, dis_min), ...} TODO: 这个可能会使用
        # teacher_avg_min = self.cal_teacher_patent_dist(teacher_all_patent)

        for teacher_id in self.teacher_basic_info.keys():
            self.teacher_basic_info[teacher_id]["achieve_nums"] = len(teacher_all_patent[teacher_id])
            self.teacher_basic_info[teacher_id]["patent_list"] = self.get_patent_by_teacher_id(teacher_id)

        # 3. 获取项目的信息，并将老师对应的项目信息添加到对应的字典中
        project_info = self.patentDao.get_teacher_project_info()
        for dic in project_info:
            teacher_id = dic["teacher_id"]
            if "project_list" in self.teacher_basic_info[teacher_id].keys():
                self.teacher_basic_info[teacher_id]["project_list"].append(dic["project_name"])
            else:
                self.teacher_basic_info[teacher_id]["project_list"] = [dic["project_name"]]

        team_list = self.construct_team_info()
        school_proportion = self.get_school_proportion(team_list)  # 获取每个学校的相似成果个数
        return {"team_list": team_list, "teacher_basic_info": self.teacher_basic_info, "patent_info": self.get_patent_info(), "school_proportion": school_proportion}

    def get_school_proportion(self, team_list):
        """
        获取搜索结果中各个学校对应的专利数量
        :return:
        """
        school_patent_num = {}
        school_set = {0}
        for dic in team_list:
            school = dic["school"]
            nums = dic["achieve_nums"]
            if school in school_patent_num.keys():
                school_patent_num[school] += nums
            else:
                school_set.add(school)
                school_patent_num[school] = nums
        school_set.remove(0)
        data = [{"name": school, "value": nums} for school, nums in school_patent_num.items()]
        return {
            "legend": list(school_set),
            "series": data,
            "seriesName": "学校数量占比"
        }

    def get_patent_by_teacher_id(self, teacher_id):
        """
        根据teacher_id 从teacher_patent中获取搜索结果中该教师的专利列表
        :param teacher_id:
        :return:
        """
        return_list = []  # 该教师对应的专利列表
        for d in self.teacher_patent:
            if teacher_id == d["teacher_id"]:
                return_list.append({
                    "patent_name": d["patent_name"],
                    "patent_id": d["patent_id"]
                })
        return return_list

    def get_teacher_team(self):
        """
        获取搜索到的教师列表中的团队
        :return: {
            team_id1: {"member_id_list":[t1_id, t2_id], ...},
            ...
        }
        """
        teacher_id_list = self.compose_teacher_id_list()
        teacher_team_list = RelationshipService.get_team_ids_by_teacher_ids(teacher_id_list)  # [{"teacher.team": team_id, "teacher.id": t_id}, ...]
        team = {}
        no_team_list = []
        for dic in teacher_team_list:
            team_id = dic["teacher.team"]
            teacher_id = dic["teacher.id"]
            if team_id is None:  # 该教师没有团队
                no_team_list.append(teacher_id)
                continue
            if team_id in team.keys():
                team[team_id]["member_id_list"].append(teacher_id)
            else:
                team[team_id] = {"member_id_list": [teacher_id], "team_id": team_id}
        # TODO: no_team的如何处理？？
        return team

    def compose_teacher_id_list(self):
        """
        从[{"teacher_id": **, "teacher_name": **, "patent_id": **, ..}, {..}, ..]中提取出teacher_id_list
        :return: [t1_id, t2_id, ...]
        """
        teacher_list = self.teacher_patent
        teacher_id_list = []
        for teacher in teacher_list:
            teacher_id = teacher["teacher_id"]
            teacher_id_list.append(teacher_id)
        return teacher_id_list

    def construct_team_info(self):
        """
        获取该团队的相关信息，通过团队中的每个人相应信息出现的频次
        相关信息包括： 所在学校；所在学院；依托平台；工程技术中心（可能没有）
        :return:
        """
        team_dict = self.get_teacher_team()
        team_dict = self.cal_team_org(team_dict)  # 计算团队所在的组织（学校/学院）以及拥有的平台（实验室）
        team_dict = self.cal_team_similar_patent_list(team_dict)  # 获取该团队拥有的相似专利列表， 添加到对应的team
        team_dict = self.cal_team_project_info(team_dict)  # 计算该团队拥有的项目信息，添加到对应的team
        team_list = self.cal_composite_score(team_dict)
        return team_list

    def cal_composite_score(self, team_dict):
        """
        计算每个团队的综合分数，并排序
        目前分数计算 直接使用该团队的相似成果数量
        :param team_dict:
        :return:
        """
        for team_id in team_dict.keys():
            # TODO: 更改计算分数
            team_dict[team_id]["score"] = team_dict[team_id]["achieve_nums"]
        team_list = [team_dict[team_id] for team_id in team_dict.keys()]  # 字典转成列表
        team_list = sorted(team_list, key=lambda e: e["score"], reverse=True)
        return team_list

    def cal_team_similar_patent_list(self, team_dict):
        """
        计算该团队所拥有的相似专利列表
        :return:
        """
        for team_id in team_dict.keys():
            teacher_id_list = team_dict[team_id]["member_id_list"]
            patent_set = {0}
            for teacher_id in teacher_id_list:
                patent_list = self.teacher_basic_info[teacher_id]["patent_list"]
                for patent in patent_list:
                    patent_id = patent["patent_id"]
                    patent_set.add(patent_id)
            patent_set.remove(0)
            team_dict[team_id]["patent_id_list"] = list(patent_set)
            team_dict[team_id]["achieve_nums"] = len(list(patent_set))
        return team_dict

    def cal_team_org(self, team_dict):
        """
        计算团队所在的组织（学校/学院）以及拥有的平台（实验室）
        :return:
        """
        # 获取多个教师的基本信息
        teacher_basic_info = self.teacher_basic_info

        for team_id, info in team_dict.items():
            # 对于每一个团队，获取团队中的每个成员的学校 学院 实验室信息，计算出现的频次，取频次最高的作为该团队的相应标识
            school_dict = {}
            institution_dict = {}
            lab_dict = {}
            for teacher_id in info["member_id_list"]:
                school = teacher_basic_info[teacher_id]["school"]
                institution = teacher_basic_info[teacher_id]["institution"]
                lab = teacher_basic_info[teacher_id]["lab"]
                if school is not None and school != "":
                    if school in school_dict.keys():
                        school_dict[school] += 1
                    else:
                        school_dict[school] = 1

                if institution is not None and school != "":
                    if institution in institution_dict.keys():
                        institution_dict[institution] += 1
                    else:
                        institution_dict[institution] = 1

                if lab is not None and school != "":
                    if lab in lab_dict.keys():
                        lab_dict[lab] += 1
                    else:
                        lab_dict[lab] = 1
            school = self.get_max_value_key(school_dict)
            institution = self.get_max_value_key(institution_dict)
            lab = self.get_max_value_key(lab_dict)
            team_dict[team_id]["school"] = school
            team_dict[team_id]["institution"] = institution
            team_dict[team_id]["lab"] = lab
        return team_dict

    def cal_team_project_info(self, team_dict):
        """
        计算一个团队内的项目信息
        :return:
        """
        for team_id in team_dict.keys():
            teacher_id_list = team_dict[team_id]["member_id_list"]
            project_set = {0}
            for teacher_id in teacher_id_list:
                if "project_list" not in self.teacher_basic_info[teacher_id].keys():  # 该教师没有项目
                    continue
                project_list = self.teacher_basic_info[teacher_id]["project_list"]
                for project in project_list:
                    project_set.add(project)
            project_set.remove(0)
            team_dict[team_id]["project_list"] = list(project_set)
        return team_dict

    def get_max_value_key(self, _dict):
        """
        获取字典中最大值对应的键，并返回该键
        :return:
        """
        max_times = 0
        key = ""
        for temp_key, _times in _dict.items():
            if max_times < _times:
                key = temp_key
                max_times = _times
        return key


if __name__ == '__main__':
    s = PatentSearchService("空调系统")
    s.construct_teacher_in_res()
