import pytest
from web.dao.review_submit import *


def test_get_unread_records_num(init_test_app):
    data = get_unread_records_num(department_id=1)
    assert len(data) == 1
    assert data[0]["count"] > 0


if __name__ == '__main__':
    pytest.main([__file__, '-s'])
