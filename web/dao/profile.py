from web.extensions import mysql


def get_school_discipline(school):
    """
    获取学校的重点学科
    :param school:
    :return:
    """
    sql = """
        select s.name, d.discipline, d.result
        from discipline_assess d
        LEFT JOIN school s
        on d.school_id = s.id
        where s.name = ? and d.result like "A%%" 
    """
    return mysql.select(sql, school)


def get_school_lab(school):
    """
    获取学院的实验平台
    :param school:
    :return:
    """
    sql = """
        select i.lab
        from clean_inventor_backup i
        LEFT JOIN school s
        on i.school_id = s.id
        where s.name = ? and i.lab is not null and i.lab != ""
        GROUP BY lab
    """
    return mysql.select(sql, school)


def get_institution_patent_num(school):
    """
    获取某一学校各学院的专利数量
    :return:
    """
    sql = """
        select t.institution, t.cnt
        from 
        (
        select i.institution, count(i.institution) cnt
        from clean_inventor_backup i
        LEFT JOIN school s
        on i.school_id = s.id
        LEFT JOIN c_inventor_patent_backup ip
        on i.id = ip.inventor_id
        LEFT JOIN patent p
        on ip.patent_id = p.id
        where s.name = ? and i.institution is not null and i.institution != ""
        GROUP BY i.institution
        ORDER BY cnt desc
        ) t
        where t.cnt > 500
    """
    return mysql.select(sql, school)


def get_institution_teacher_id(school, institution):
    """
    获取这个学院下的所有人 id
    :param school:
    :param institution:
    :return:
    """
    sql = """
        select  i.id teacher_id
        from clean_inventor_backup i
        LEFT JOIN school s
        on i.school_id = s.id
        LEFT JOIN c_inventor_patent_backup ip
        on i.id = ip.inventor_id
        where s.name = ? and i.institution = ?
        GROUP BY i.id
    """
    return mysql.select(sql, school, institution)


def get_institution_teacher_ids(school, institution):
    """
    获取该学校该学院下的老师id
    :param school:
    :param institution:
    :return:
    """
    sql = """
        select i.id
        from clean_inventor_backup i
        LEFT JOIN school s
        on i.school_id = s.id
        where s.name = ? and i.institution = ?
    """
    return mysql.select(sql, school, institution)


def get_labs_honors_by_teacher_ids(teacher_ids):
    """
    获取教师的实验平台信息， 荣誉信息（院士，长江...)
    :param teacher_ids:
    :return:
    """
    sql = """
        select lab, honor
        from clean_inventor_backup 
        where id in (
    """
    if len(teacher_ids) == 0:
        return []
    for _id in teacher_ids:
        sql += str(_id) + ","
    sql = sql[0:-1]
    sql += ")"
    return mysql.select(sql)


def get_patent_num_by_teacher_ids(teacher_ids):
    """
    获取多个教师的所有专利id,以此获取其成果数量
    :param teacher_ids:
    :return:
    """
    sql = """
        select ip.patent_id
        from clean_inventor_backup i
        LEFT JOIN c_inventor_patent_backup ip
        on i.id = ip.inventor_id
        where i.id in (
    """
    if len(teacher_ids) == 0:
        return []
    for _id in teacher_ids:
        sql += str(_id) + ","
    sql = sql[0:-1]
    sql += ") GROUP BY ip.patent_id"
    return mysql.select(sql)


def get_good_discipline_num_by_school(school):
    """
    获取这些学校的一流学科数量
    :param school:
    :return:
    """
    sql = """
        select count(1) cnt
        from discipline_assess
        where school = ? and result like "A%%" 
    """
    return mysql.select(sql, school)
