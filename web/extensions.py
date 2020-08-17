from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from web.utils.mysql import MySQL

bootstrap = Bootstrap()
mysql = MySQL()
login_manager = LoginManager()

# 当访问到受login_required时默认跳转到下面的视图
login_manager.login_view = 'auth.login'
login_manager.login_message = None
login_manager.login_message_category = None