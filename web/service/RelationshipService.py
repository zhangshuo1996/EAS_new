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

def get_teacher_net(teacher_id):
    """
    获取教师的个人网络关系
    :return:
    """
    data = NeoOperator.get_ego_net(teacher_id)
    # print(pprint.pformat(data))
    res = format2Echarts(data)
    return res

if __name__ == '__main__':
    get_teacher_net(152837)