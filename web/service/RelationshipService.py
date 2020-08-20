from web.utils.Ego_net import *


def format2Echarts(data):
    """
    将返回数据格式化为Echarts适配的格式
    :param data:

    :return:
     dict {
            "nodes": [
                {id, name, ....}, ...
            ],

            "links": [
                {"source": xx, "target": xxx}, ...
            ]

        }
    """
    result = {"nodes":[], "links": []}
    if len(data) == 0:
        return result
    print(data)
    center_node = dict(data[0]["nodes"][0])

    result["nodes"].append(center_node)

    for item in data:
        target_node = dict(item["nodes"][1])
        result["nodes"].append(target_node)

        relation = dict(item["relationship"][0])
        result["links"].append({"source": center_node['id'], "target": target_node["id"], "value": relation})

    return result


def get_teacher_team(teacher_id):
    """
    获取教师的所在团队的教师id
    :return:
    """
    data = NeoOperator.get_this_teacher_team_id(teacher_id)
    if len(data) == 0 or data[0]["teacher.team"] is None:  # 该教师没有team_id，无团队
        return {0}
    team_id = data[0]["teacher.team"]
    teacher_ids = NeoOperator.get_team_member_id(team_id)
    team = convert_team_to_set(teacher_ids)
    return team


def convert_team_to_set(teacher_ids):
    """
    将团队中的列表形式转化为集合形式{t1, t2, t3}
    :param teacher_ids:
    :return:
    """
    team = {0}
    for dic in teacher_ids:
        teacher_id = dic["teacher.id"]
        team.add(teacher_id)
    return team




if __name__ == '__main__':
    # get_teacher_net(125009)
    get_teacher_team(9961)