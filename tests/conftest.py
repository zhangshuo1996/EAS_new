import pytest
from web import create_app


@pytest.fixture(scope='session')
def init_test_app():
    app = create_app('testing')
    context = app.test_request_context()
    context.push()
    client = app.test_client()
    runner = app.test_cli_runner()
    # TODO: 暂时只返回client pytest再次调用以清除环境
    yield client
    context.pop()


