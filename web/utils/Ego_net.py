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

    @classmethod
    def get_this_teacher_net(cls, teacher_id):
        """
        根据教师的id获取与其团队中的其他教师id
        :return:
        """
        try:
            cql = "Match p=(:Teacher{id:%s}) return NODES(p) as nodes, RELATIONSHIPS(p) as relationship" % str(teacher_id)
            back = NeoOperator.graph.run(cql).data()
            return back
        except Exception as e:
            print(e)

    @classmethod
    def get_this_teacher_team_id(cls, teacher_id):
        """
        获取该教师所在团队的team_id
        :param teacher_id:
        :return:
        """
        try:
            cql = "match (teacher:Teacher) where teacher.id = %s return teacher.team" % str(teacher_id)
            back = NeoOperator.graph.run(cql).data()
            return back
        except Exception as e:
            print(e)

    @classmethod
    def get_team_member_id(cls, team_id):
        """
        根据team_id获取该团队下的所有成员id
        :param team_id:
        :return:
        """
        try:
            cql = "match (teacher:Teacher) where teacher.team = %s return teacher.id" % str(team_id)
            back = NeoOperator.graph.run(cql).data()
            return back
        except Exception as e:
            print(e)


def get_team_ids_by_teacher_ids(teacher_id_list):
    """
    根据teacher_ids 获取这些teacher对应的团队team_ids
    :return:[{"teacher.team": team_id, "teacher.id": t_id}]
    """
    try:
        cql = "match (teacher:Teacher) where teacher.id in [{ids_str}] return teacher.team, teacher.id"
        cql = compose_cql(cql, teacher_id_list)
        back = NeoOperator.graph.run(cql).data()
        return back
    except Exception as e:
        print(e)


def get_cooperate_rel_teacher_ids(teacher_id_list):
    """
    根据teacher_ids 获取这些teacher的合著关系
    :return:
    """
    try:
        cql = """
            Match p=(t:Teacher)-[r:cooperate]-(:Teacher) 
            where t.id in [{ids_str}]
            return NODES(p) as nodes, RELATIONSHIPS(p) as relationship
        """
        cql = compose_cql(cql, teacher_id_list)
        print(cql)
        back = NeoOperator.graph.run(cql).data()
        return back
    except Exception as e:
        print(e)


def get_cooperate_rel_by_team_id_list(team_id_list, institution, patent_num):
    """
    根据学院中的team_id_list 获取 学院内部的社区关系
    :param patent_num:
    :param institution:
    :param team_id_list:
    :return:
    """
    try:
        cql = """
                   match p=(t1:Teacher)-[r:cooperate]-(t2:Teacher) 
                    where t1.team in [{ids_str}] and t2.team in [{ids_str}] 
                    and t1.patent > 0 and t1.institution = "{institution}" and t2.institution = "{institution}" 
                    and t1.patent > {patent_num} and t2.patent > {patent_num}
                    return NODES(p) as nodes, RELATIONSHIPS(p) as relationship
                """
        cql = compose_cql2(cql, team_id_list, institution, patent_num)
        print(cql)
        back = NeoOperator.graph.run(cql).data()
        return back
    except Exception as e:
        print(e)


def compose_cql2(cql, _list, institution, patent_num):
    """
    组合查询cql中有in的语句,
    :param patent_num:
    :param institution:
    :param _list:
    :param cql:
    :return:
    """
    ids_str = ""
    for _id in _list:
        ids_str += str(_id) + ","
    ids_str = ids_str[0:-1]
    return cql.format(ids_str=ids_str, institution=institution, patent_num=patent_num)


def compose_cql(cql, _list):
    """
    组合查询cql中有in的语句,
    :param _list:
    :param cql:
    :return:
    """
    ids_str = ""
    for _id in _list:
        ids_str += str(_id) + ","
    ids_str = ids_str[0:-1]
    return cql.format(ids_str=ids_str)


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
