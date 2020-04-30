import pytest
from flask import url_for

#
# def test_count_patents_with_ipc(init_test_app):
#     client = init_test_app
#     response = client.get(url_for('intellectual_property.get_patent_counts_with_depth', depth=0))
#     json_data = response.get_json()
#
#     assert 'error' not in json_data
#     assert len(json_data) == 8
#
#
# def test_count_patents_with_ipc_invalid(init_test_app):
#     client = init_test_app
#     response = client.get(url_for('intellectual_property.get_patent_counts_with_depth', depth=3))
#     json_data = response.get_json()
#
#     assert 'error' in json_data


# def test_distribute_task(init_test_app):
#     client = init_test_app
#     data = {"server-name": "1", "task-name": "实用新型", "task-goal": "123",
#             "deadline": "2020-03-28", "principal": "负责人1", "task-id": "-1"}
#     response = client.post('/distribute_task', data=data)
#     json_data = response.get_json()
#     assert 'success' in json_data
#
#     del data["deadline"]
#     response = client.post('/distribute_task', data=data)
#     json_data = response.get_json()
#     assert 'error' in json_data


if __name__ == '__main__':
    pytest.main([__file__, '-s'])
