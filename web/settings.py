import os
import logging
from web.config import MYSQL_CONFIG, MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB, MYSQL_CURSORCLASS

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


class BaseConfig(object):
    # wtform库用于CSRF
    SECRET_KEY = os.getenv('SECRET_KEY', "secret key")
    # 文件上传路径
    FILE_UPLOAD_PATH = os.path.join(basedir, 'uploads')
    SCHOOL_AVATAR_PATH = os.path.join(basedir, 'school_avatar')
    MYSQL_CONFIG = MYSQL_CONFIG


# class DevelopmentConfig(BaseConfig):
#     """开发环境配置"""
#     MYSQL_CONFIG = MYSQL_CONFIG
#     MYSQL_CONFIG['maxconnections'] = 1
#     MYSQL_CONFIG['mincached'] = 1
#     logging.basicConfig(format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s',
#                         level=logging.DEBUG)

class DevelopmentConfig(BaseConfig):
    """开发环境配置"""
    MYSQL_HOST = MYSQL_HOST
    MYSQL_PORT = MYSQL_PORT
    MYSQL_USER = MYSQL_USER
    MYSQL_PASSWORD = MYSQL_PASSWORD
    MYSQL_DB = MYSQL_DB
    MYSQL_CURSORCLASS = MYSQL_CURSORCLASS
    logging.basicConfig(format='%(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                        level=logging.DEBUG)


class TestingConfig(BaseConfig):
    """测试环境配置"""
    TESTING = True
    WTF_CSRF_ENABLED = False


class ProductionConfig(BaseConfig):
    """生产环境配置"""
    pass


configuration = {
    'development':  DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}