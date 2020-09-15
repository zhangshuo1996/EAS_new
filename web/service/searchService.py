"""
搜索相关服务
2020.08.17
by zhang
"""
from web.dao import searchDao
import json


def save_this_search_text(searcher_id, search_text):
    """
    记录此次搜索的文本
    :param searcher_id:
    :param search_text:
    :return:
    """
    outcome = searchDao.get_history_by_text(search_text)
    if outcome is None or "id" not in outcome.keys():
        outcome_id = searchDao.save_this_search_text(searcher_id, search_text)
    else:
        outcome_id = outcome["id"]
        searchDao.update_history_time(search_text)
    return outcome_id
