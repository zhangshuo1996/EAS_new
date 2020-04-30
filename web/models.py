from flask import abort
from enum import Enum, unique
from flask_login import UserMixin, current_user
from functools import wraps


class User(dict, UserMixin):
    """
    登录用户类
    """
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError("'User' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value

    def can_write(self, affair_id):
        """是否拥有写权限"""
        for permission in self.permissions:
            if permission['affair_id'] == affair_id and permission['access_right'] == 1:
                return True
        return False

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        """
        以Unicode形式返回用户的唯一标识符
        :return: str
        """
        return str(self.id)


@unique
class UserType(Enum):
    """枚举体 分为政府用户和服务商"""
    GOVERNMENT_USER = 0
    CHARGER = 1


class AffairType(object):
    INTELLECTUAL_PROPERTY = 1
    OFFICE = 2
    PRODUCE_STUDY = 3
    INCUBATOR = 4
    HIGH_TECH_ENTERPEISE = 5


# 部门id与跳转的url对应
# TODO: affair_id 与跳转的URL对应
affair_id_url = {
    AffairType.INTELLECTUAL_PROPERTY: 'intellectual_property.annual_plan',  # 知识产权科
    AffairType.PRODUCE_STUDY: 'produce_study.annual_plan',  # 产学研合作科
    AffairType.INCUBATOR: 'incubator.annual_plan',  # 孵化器
    AffairType.HIGH_TECH_ENTERPEISE: 'high_tech_enterprise.annual_plan',  # 高企科
    AffairType.OFFICE: 'office.index' # 办公室
}
affair_id_endpoints = {
    AffairType.INTELLECTUAL_PROPERTY: [
        {'name': '目标', 'endpoint': 'intellectual_property.annual_plan'},
        {'name': '计划', 'endpoint': 'intellectual_property.monthly_comparison'},
    ],
    AffairType.PRODUCE_STUDY: [
        {'name': '目标', 'endpoint': 'produce_study.annual_plan'},
        {'name': '计划', 'endpoint': 'produce_study.monthly_comparison'},
    ],
    AffairType.INCUBATOR: [
        {'name': '目标', 'endpoint': 'incubator.annual_plan'},
        {'name': '计划', 'endpoint': 'incubator.monthly_comparison'},
    ],
    AffairType.HIGH_TECH_ENTERPEISE: [
        {'name': '目标', 'endpoint': 'high_tech_enterprise.annual_plan'},
        {'name': '计划', 'endpoint': 'high_tech_enterprise.monthly_comparison'},
    ],
    AffairType.OFFICE: [
        {'name': '总览', 'endpoint': 'office.index'},
        {'name': '业务管理', 'endpoint': 'office.project_manage'},
        {'name': '服务商管理', 'endpoint': 'office.provider_manage'},
    ]
}


def user_type_required(user_type):
    def decorator(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            # 验证用户类型
            if isinstance(user_type, UserType) and user_type == current_user.type:
                return func(*args, **kwargs)
            abort(403)
        return decorated_function
    return decorator


def permission_required(affair_id):
    def decorator(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            # 验证用户类型
            is_authenticated = False
            for permission in current_user.permissions:
                if permission['affair_id'] == affair_id:
                    is_authenticated = True
                    break
            if is_authenticated:
                return func(*args, **kwargs)
            abort(403)
        return decorated_function
    return decorator
