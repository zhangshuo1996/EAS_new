import pytest
from web.service.station_news import *


def test_upsert_assignment(init_test_app):
    upsertData = {"sender_id": 1, "sender_name": "发明专利", "sender_kind": "1", "receiver_id": 5, "receiver_name": "负责人2",
                  "receiver_kind":"1", "news_content": "fdd"}
    result = add_one_record(**upsertData)
    assert "success" in result



if __name__ == '__main__':
    pytest.main([__file__, '-s'])
