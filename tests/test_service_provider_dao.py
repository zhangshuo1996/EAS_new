import pytest
import sys
import os
from web.dao.service_provider import *


# def test_get_departments(init_test_app):
#     department_ids = [1]
#     departments = get_departments(department_ids)
#
#     assert len(departments) == 1
#     department = departments[0]
#     assert 'id' in department
#     assert 'department' in department
#
#
# def test_get_assignments_by_charger(init_test_app):
#     charger_id = 1
#     tasks = get_assignments(charger_id)
#
#     assert len(tasks) != 0
#     for task in tasks:
#         assert 'type' in task


def test_get_records(init_test_app):
    records = get_records(charger_id=1)
    for record in records:
        assert "submit_time" in record


def test_get_departments(init_test_app):
    department_ids = [1]
    departments = get_departments(department_ids)

    assert len(departments) == 1
    department = departments[0]
    assert 'id' in department
    assert 'department' in department


def test_get_assignments_by_charger(init_test_app):
    charger_id = 1
    tasks = get_assignments(charger_id)

    assert len(tasks) != 0
    for task in tasks:
        assert 'type' in task
        assert 'task_id' in task


if __name__ == '__main__':
    pytest.main([__file__, '-s'])
