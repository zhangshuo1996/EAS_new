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
