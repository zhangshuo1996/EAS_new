from web.extensions import mysql


def save_this_search_text(searcher_id, search_text):
    """
    记录此次搜索的文本
    :param searcher_id:
    :param search_text:
    :return:
    """
    sql = """
        insert into search_history
        (searcher_id, search_text, gmt_create)
        values (?, ?, now())
    """
    return mysql.insert(sql, searcher_id, search_text)


def get_history_by_text(search_text):
    """
    判断是否存在相似的文本
    :param input_key:
    :return:
    """
    sql = """
        select count(1) cnt
        from search_history
        where search_text = ?
    """
    return mysql.select_one(sql, search_text)


def update_history_time(search_text):
    """
    更新该搜索文本所在行的时间
    :param search_text:
    :return:
    """
    sql = """
        update search_history
        set gmt_create = now()
        where search_text = ?
    """
    return mysql.update(sql, search_text)
