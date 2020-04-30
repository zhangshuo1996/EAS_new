import pytest
from web.service.intellectual_property import *


# def test_count_patents_with_ipc(init_test_app):
#     results = count_patents_with_ipc(depth=0)
#
#     assert isinstance(results, list)
#     assert len(results) == 9
#     first_datum = results[0]
#     # 必须包含 code amount desc
#     assert 'code' in first_datum
#     assert 'amount' in first_datum
#     assert 'title' in first_datum


# def test_upsert_assignment(init_test_app):
#     upsertData = {"task_id": -1, "name": "发明专利", "goal": 30, "charger_id": 5, "charger_name": "负责人2", "deadline": "2020/03/28", "department_id": 2}
#     result = upsert_assignment(**upsertData)
#     assert "success" in result
#
#     # upsertData["task_id"] = "a"
#     upsertData["deadline"] = "2020/03/28"
#
#     error_insert = upsert_assignment(**upsertData)
#     assert "error" in error_insert
#
#     upsertData["task_id"] = 2
#     update_result = upsert_assignment(**upsertData)
#     assert "success" in update_result

#
# def test_get_progress_rate(init_test_app):
#     back = get_progress_rate(target_id=2, year=2020)
#     print(back)


# def test_get_progress(init_test_app):
#     back = get_progress(target_id=2, year=2020)
#     print(back)

def test_get_service_situation(init_test_app):
    data = get_service_situation(1, start=1585699200, end=1588204800)
    assert len(data) == 4


if __name__ == '__main__':
    pytest.main([__file__, '-s'])
