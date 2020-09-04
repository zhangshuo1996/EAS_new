from web.utils import Ego_net as ego_net


def format2Echarts(_data):
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
    result = {
        "nodes": [],
        "links": []
    }
    if len(_data) == 0:
        return result
    center_node = dict(_data[0]["nodes"][0])

    result["nodes"].append(center_node)

    for item in _data:
        target_node = dict(item["nodes"][1])
        result["nodes"].append(target_node)

        relation = dict(item["relationship"][0])
        result["links"].append({"source": center_node['id'], "target": target_node["id"], "value": relation})

    return result


def format2echarts(_data):
    """
    将返回数据(多个成员的社交关系)格式化为Echarts适配的格式
    :param _data:

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
    result = {
        "nodes": [],
        "links": []
    }
    if len(_data) == 0:
        return result
    node_dict = {}
    for item in _data:
        teacher_id1 = item["nodes"][0]["id"]
        teacher_id2 = item["nodes"][1]["id"]
        # 获取节点
        if teacher_id1 not in node_dict.keys():
            node_dict[teacher_id1] = item["nodes"][0]
        if teacher_id2 not in node_dict.keys():
            node_dict[teacher_id2] = item["nodes"][1]

        # 获取关系
        result["links"].append({
            "source": teacher_id1,
            "target": teacher_id2,
            "value": item["relationship"][0]["frequency"]
        })
    nodes = [val for key, val in node_dict.items()]
    result["nodes"] = nodes
    return result


def get_teacher_team(teacher_id):
    """
    获取教师的所在团队的教师id
    :return:
    """
    _data = ego_net.NeoOperator.get_this_teacher_team_id(teacher_id)
    if len(_data) == 0 or _data[0]["teacher.team"] is None:  # 该教师没有team_id，无团队
        return {0}
    team_id = _data[0]["teacher.team"]
    teacher_ids = ego_net.NeoOperator.get_team_member_id(team_id)
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


def get_cooperate_rel(teacher_id_list):
    """
    根据teacher_ids 获取这些teacher的合著关系
    :param teacher_id_list:
    :return:
    """
    _data = ego_net.get_cooperate_rel_teacher_ids(teacher_id_list)
    result = format2echarts(_data)
    return result


def get_cooperate_rel_by_team_id_list(team_id_list, institution):
    """
    根据学院中的team_id_list 获取 学院内部的社区关系
    :param institution:
    :param team_id_list:
    :return:
    """
    _data = ego_net.get_cooperate_rel_by_team_id_list(team_id_list, institution, 0)
    result = format2echarts(_data)
    if len(result["nodes"]) > 70:
        _data = ego_net.get_cooperate_rel_by_team_id_list(team_id_list, institution, 3)
        result = format2echarts(_data)
    if len(result["nodes"]) > 70:
        _data = ego_net.get_cooperate_rel_by_team_id_list(team_id_list, institution, 5)
        result = format2echarts(_data)
    if len(result["nodes"]) > 70:
        _data = ego_net.get_cooperate_rel_by_team_id_list(team_id_list, institution, 8)
        result = format2echarts(_data)
    return result


def get_team_ids_by_teacher_ids(teacher_id_list):
    """
    根据教师的id列表获取这些教师对应的team_id
    :param teacher_id_list:
    :return:
    """
    team_ids = ego_net.get_team_ids_by_teacher_ids(teacher_id_list)
    # team_id_list = [dic["teacher.team"] for dic in team_ids]
    return team_ids


def get_team_id_list_by_teacher_ids(teacher_id_list):
    """
    根据教师的id列表获取这些教师对应的team_id
    :param teacher_id_list:
    :return:[team_id1, team_id2, ...]
    """
    team_ids = ego_net.get_team_ids_by_teacher_ids(teacher_id_list)
    team_id_list = []
    for dic in team_ids:
        if dic["teacher.team"] is not None:
            team_id_list.append(dic["teacher.team"])
    return team_id_list


if __name__ == '__main__':
    get_teacher_team(9961)
