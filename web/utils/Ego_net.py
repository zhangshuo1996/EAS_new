from py2neo import Graph
from web.config import NEO_CHEN
import pprint


class NeoOperator(object):

    graph = Graph(NEO_CHEN["host"], auth=(NEO_CHEN["user"], NEO_CHEN["password"]))

    @classmethod
    def get_ego_net(cls, teacher_id):
        """
        根据教师id获取个人中心网络
        :param teacher_id:
        :return:
        [
            {
                "nodes": [Node tyep element, Node type element2],
                "relationship": []
            },...
        ]
        """
        try:
            cql = "Match p=(:Teacher{id:%s})-[r:学术合作]-(:Teacher) return NODES(p) as nodes," \
                  " RELATIONSHIPS(p) as relationship" % teacher_id
            back = NeoOperator.graph.run(cql).data()
            return back
        except Exception as e:
            print(e)


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

    center_node = dict(data[0]["nodes"][0])
    result["nodes"].append(center_node)

    for item in data:
        target_node = dict(item["nodes"][1])
        result["nodes"].append(target_node)

        relation = dict(item["relationship"][0])
        result["links"].append({"source": center_node['id'], "target": target_node["id"], "value": relation})

    return result


if __name__ == '__main__':
    data = NeoOperator.get_ego_net(86791)
    print(pprint.pformat(data))
    res = format2Echarts(data)
    # print(res)
