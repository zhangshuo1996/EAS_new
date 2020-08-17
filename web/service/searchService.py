"""
搜索相关服务
2020.08.17
by zhang
"""
from web.dao import searchDao


def save_this_search_text(searcher_id, search_text):
    """
    记录此次搜索的文本
    :param searcher_id:
    :param search_text:
    :return:
    """
    result = searchDao.save_this_search_text(searcher_id, search_text)
    return result
