"""
@author: zs
@date: 2020.2.11
"""
import requests
import json
import sys
sys.path.append("..")
from web.dao.PaperDAO import PaperDAO


class PaperSearchService():
    """
    为搜索提供服务
    """
    paper_id_list = []
    distance_list = []
    id_dis_dict = {}
    teacher_paper = []
    paperDao = None

    def __init__(self, input_key):
        """
        初始化service
        :param input_key:
        """

        self.get_ids_by_input(input_key)  # 调用restful服务获得相似的成果id
        self.combine_id_distance()
        self.paperDao = PaperDAO(self.paper_id_list)
        self.teacher_paper = self.paperDao.return_teacher_paper()

    def get_ids_by_input(self, input):
        """
        根据用户的输入内容, 通过调用restful服务获取与之相关的成果id
        :return:
        """
        data = {"type": "search", "K": 100, "key": input}
        url = "http://39.100.224.138:6438/paper"
        data_json = json.dumps(data)
        headers = {'Content-type': 'application/json'}
        response = requests.post(url, data=data_json, headers=headers)
        i_string = eval(response.text)["I"]  # 返回的成果ID列表（字符串形式）
        d_string = eval(response.text)["D"]  # 返回的成果距离列表 （字符串形式）
        i_list = eval(i_string)
        d_list = eval(d_string)
        # print(i_list)
        # print(d_list)
        print("-----------------------------------get_ids_by_input--相似成果id获取成功-----------------------------------")
        self.paper_id_list = i_list[0]
        self.distance_list = d_list[0]

    def combine_id_distance(self):
        """
        将id列表与distance列表组合成字典
        :return: {id1: dis1, id2: dis2, ...}
        """
        for i in range(len(self.paper_id_list)):
            if self.paper_id_list[i] not in self.id_dis_dict.keys():
                self.id_dis_dict[self.paper_id_list[i]] = self.distance_list[i]

    def construct_teacher_in_res(self):
        """
        构造位于返回结果中的教师的信息
        {
            "teacher_id": ***,
            "basic_info": { "school": school,
                            "institution": institution,
                            "school_id": school_id,
                            "institution_id": institution_id,
                            "name": name
                        },
            "paper_info": [ (id1, dis1),
                            (id2, dis2)
                            ...
                          ],
            "achieve_nums": ***  # 相似成果数量
            "dis_average": ***, # 平均距离
            "dis_min": ***      # 最小距离
        }
        :return:
        """
        print("-------------------------------------construct_teacher_in_res----------------------------------")
        # 1. find 专家对应的所有成果 --> {teacher_id1: [paper_id1, paper_id2],}
        teacher_all_paper = {}
        teacher_paper = self.teacher_paper
        for d in teacher_paper:
            teacher_id = d["teacher_id"]
            paper_id = d["paper_id"]
            if teacher_id not in teacher_all_paper.keys():
                teacher_all_paper[teacher_id] = [paper_id]
            else:
                tmp_list = teacher_all_paper[teacher_id]
                tmp_list.append(paper_id)
                teacher_all_paper[teacher_id] = tmp_list
        # print(teacher_all_paper)

        # 2. construct 平均距离和最小距离字典teacher_avg_min --> {teacher_id: (dis_average, dis_min), ...}
        teacher_avg_min = {}
        for teacher_id in teacher_all_paper:
            sum_dis = 0
            min_dis = 100000000
            for paper_id in teacher_all_paper[teacher_id]:
                sum_dis += self.id_dis_dict[paper_id]
                min_dis = min(min_dis, self.id_dis_dict[paper_id])
            dis_avg = sum_dis / len(teacher_all_paper[teacher_id])
            teacher_avg_min[teacher_id] = (dis_avg, min_dis)

        # print(teacher_avg_min)
        # print(self.id_dis_dict)
        # 3. 将上面的结果： teacher_all_paper, teacher_avg_min 和teacher_info 组合
        teacher_basic_info = self.paperDao.get_teacher_basic_info()
        teacher_info_list = []  # 最终待返回的与给定结果相关的教师信息：
        for teacher_id in teacher_all_paper:
            teacher_info = {}
            teacher_info["id"] = teacher_id
            teacher_info["basic_info"] = teacher_basic_info[teacher_id]
            teacher_info["achieve_nums"] = len(teacher_all_paper[teacher_id])  # 教师个人成果数量
            teacher_info["dis_average"] = teacher_avg_min[teacher_id][0]  # 平均距离
            teacher_info["dis_min"] = teacher_avg_min[teacher_id][1]  # 最小距离
            # TODO: 综合打分？？
            # teacher_info["score"] =

            teacher_info_list.append(teacher_info)
        # print(teacher_info_list)
        teacher_info_list.sort(key=lambda info: info["achieve_nums"], reverse=True)  # 按照成果数量排序
        print(teacher_info_list)
        return teacher_info_list

    def construct_institution_info(self):
        """
        构建要返回的相关的institution信息
        :return:
        """
        print("-------------------------------------construct_institution_info----------------------------------")
        teacher_info_list = self.construct_teacher_in_res()
        # print(teacher_info_list)
        institution_info_dict = {}
        for teacher_info in teacher_info_list:
            institution_id = teacher_info["basic_info"]["institution_id"]
            if institution_id in institution_info_dict.keys():
                tmp_list = institution_info_dict[institution_id]
                tmp_list.append(teacher_info)
                institution_info_dict[institution_id] = tmp_list
            else:
                institution_info_dict[institution_id] = [teacher_info]
        # print(institution_info_dict)
        institution_output_list = []
        for institution_id in institution_info_dict.keys():
            institution_info = institution_info_dict[institution_id]
            institution_output_dict = {}
            dis_sum_avg = 0
            dis_min = 0
            achieve_nums = 0
            for institution in institution_info:
                dis_sum_avg += institution["dis_average"]
                dis_min = min(dis_min, institution["dis_min"])
                achieve_nums += institution["achieve_nums"]
            institution_output_dict["id"] = institution_id
            institution_output_dict["institution_name"] = institution_info[0]['basic_info']['institution']
            institution_output_dict["school_name"] = institution_info[0]['basic_info']['school']
            institution_output_dict["school_id"] = institution_info[0]['basic_info']['school_id']
            institution_output_dict["teacher_nums"] = len(institution_info)
            institution_output_dict["achieve_nums"] = achieve_nums
            institution_output_dict["dis_average"] = dis_sum_avg / len(institution_info)
            # institution_output_dict["teacher_list"] = institution_info_dict[institution_id]  # 教师的个人信息是否有必要加？
            institution_output_dict["dis_min"] = dis_min
            # TODO: 学院的综合评分
            institution_output_list.append(institution_output_dict)
        institution_output_list.sort(key=lambda info: info["achieve_nums"], reverse=True)
        print(institution_output_list)
        return institution_output_list


if __name__ == '__main__':
    s = PaperSearchService("空调系统")
    s.construct_teacher_in_res()
    s.construct_institution_info()
