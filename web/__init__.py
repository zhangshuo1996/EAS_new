import os
from flask import Flask, render_template, current_app, url_for
from web.blueprints.search import search_bp
from web.blueprints.auth import auth_bp
from web.settings import configuration
from web.extensions import bootstrap
from web.extensions import login_manager
from web.utils import db
from web.models import UserType, AffairType, affair_id_endpoints
from web.config import DB_CONFIG


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', "development")

    app = Flask('web')
    app.config.from_object(configuration[config_name])

    # 初始化数据库连接池
    db.create_engine(**DB_CONFIG)

    # 注册日志处理器
    register_logger(app)
    # 初始化扩展
    register_extensions(app)

    # 注册蓝图
    register_blueprints(app)
    # 注册错误处理函数
    register_errors(app)
    # 注册模板上下文处理函数
    register_template_context(app)
    # 注册命令
    register_commands(app)
    # 注册shell
    register_shell_context(app)

    return app


def register_logger(app):
    pass


def register_extensions(app):
    bootstrap.init_app(app)
    login_manager.init_app(app)


def register_blueprints(app):
    app.register_blueprint(auth_bp, url_prefix='/')
    app.register_blueprint(search_bp, url_prefix='/search')


def register_errors(app):
    # @app.errorhandler(404)
    # def bad_request(error):
    #     return render_template('errors/404.html', error=error), 404
    #
    # @app.errorhandler(400)
    # def bad_request(error):
    #     return render_template('errors/400.html', error=error), 400
    pass


def register_shell_context(app):
    pass


def register_commands(app):
    pass


def register_template_context(app):
    """注册模板上下文"""
    pass
    # @app.template_test()
    # def prefix_match(request_endpoint, datum):
    #     """验证前缀是否相同"""
    #     endpoint = datum['endpoint']
    #     return request_endpoint.startswith(endpoint.split('.')[0])

    # @app.context_processor
    # def make_template_context():
    #     extras = {}
    #     # 获取用户未读消息数量
    #     unread_records, unread_msg = 0, 0
    #     if not current_user.is_anonymous:
    #         user_id = current_user.id
    #         user_name = current_user.name
    #         # TODO: 服务商用户的未读消息设置？？
    #         if int(user_id) >= 1000000:
    #             pass
    #         else:
    #             unread_msg = station_news_service.get_count_unchecked_news(int(user_id), user_name)
    #             department_id = current_user.department_id
    #             unread_records = review_submit_service.get_unread_records_num(department_id)
    #             # 合并affairs
    #             affairs = current_user.permissions.copy()
    #             for affair in affairs:
    #                 endpoints = affair_id_endpoints[affair['affair_id']]
    #                 affair['endpoints'] = endpoints
    #             extras['affairs'] = affairs
    #
    #     return dict(unread_records=unread_records, unread_msg=unread_msg,
    #                 UserType=UserType, AffairType=AffairType, **extras)

    # @app.context_processor
    # def inject_url():
    #     return {
    #         'url_for': dated_url_for
    #     }


# def dated_url_for(endpoint, **kwargs):
#     filename = None
#     if endpoint == 'static':
#         filename = kwargs.get('filename', None)
#     if filename:
#         input_path = os.path.join(current_app.root_path, endpoint, filename)
#         kwargs['v'] = int(os.stat(input_path).st_mtime)
#     return url_for(endpoint, **kwargs)


@login_manager.user_loader
def load_user():
    return None
