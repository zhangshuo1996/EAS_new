import pytest
import sys
import os
sys.path.append(os.getcwd())
from web.dao.intellectual_property import *


# def test_get_ipc_map(init_test_app):
#     results = get_ipc_map(depth=0)
#     assert len(results) == 8
#
#
# def test_get_total_number(init_test_app):
#     result = get_total_patent_number()
#     assert isinstance(result, int)
#     assert result > 0
#
#
# def test_count_patents_with_ipc(init_test_app):
#     ipc_list = ['A', 'B']
#     length = 1
#     results = count_patents_with_ipc(length, ipc_list, len(ipc_list))
#
#     assert isinstance(results, list)
#     assert len(results) == len(ipc_list)
#     first_datum = results[0]
#     assert 'code' in first_datum
#     assert 'amount' in first_datum
#
#
# def test_get_target_info(init_test_app):
#     result = get_target_info(1, 2020)
#     assert isinstance(result, list)
#     assert len(result) == 4
#     assert "id" in result[0] and "name" in result[0] and "numbers" in result[0]
#
#     result = get_target_info(1, 2021)
#     assert isinstance(result, tuple)
#     assert len(result) == 0


# def test_insert_year_target(init_test_app):
#     result = insert_year_target("技术需求", 600, 2020, 1)
#     assert result > 0


# def test_insert_assignment(init_test_app):
#     new_row_id = insert_assignment(type="发明专利", target=100, charger_id=1, charger_name="负责人1", deadline=1671827200, department_id=1)
#     assert new_row_id > 0

#
# def test_update_assignment(init_test_app):
#     update_row_id = update_assignment(12, "发明专利", 11, 1, "负责人1", 1671827200)
#     assert update_row_id == 1
#
#     update_row_id = update_assignment(12, "发明专利", 10, 1, "负责人1", 1671827200)
#     assert update_row_id == 0
#
#     error_row = update_assignment(0, "发明专利", "100", 1, "负责人1", 1671827200)
#     assert error_row == 0


# def test_update_assignment_status(init_test_app):
#     update_row = update_assignment_status(2, 2)
#     assert update_row == 1
#
#     update_row = update_assignment_status(2, 2)
#     assert update_row == 0
#
#     error_row = update_assignment_status(0, 2)
#     assert error_row == 0
#
#
# def test_update_assignment_progress(init_test_app):
#     update_row = update_assignment_progress(1, 1)
#     assert update_row == 1
#
#     error_row = update_assignment_progress(0, 2)
#     assert error_row == 0


# def test_get_progress_rate(init_test_app):
#     target_id, year = 2, 2020
#     data = get_progress(target_id, year)
#     print(data)

def test_get_service_situation(init_test_app):
    data = get_service_situation(1, start=1585699200, end=1588204800)
    print(data)


if __name__ == '__main__':
    pytest.main([__file__, '-s'])
