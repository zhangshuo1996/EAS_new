import pytest
from flask import url_for


def test_download(init_test_app):
    client = init_test_app
    response = client.get(url_for('review_submit.download', filename="1585573182/tool.svg"))
    print(response)


if __name__ == '__main__':
    pytest.main([__file__, '-s'])