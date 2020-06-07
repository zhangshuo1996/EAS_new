# Patent Map System
## 1. Pycharm运行配置说明
因为flask的app对象被封装在了web/\__init__.py中的工厂方法create_app中，所以需要进行一些设置才可以运行
>1. 在Pycharm中对Flask server设置（可断点调试）：
>>   1. 打开Edit Configuration
>>   2. 设置Target type => Script path。
>>   3. 设置Target => wsgi.py的完整路径。
>2. 在cmd中设置（无法断点调试）：
>>   1. set FLASK_APP=web
>>   2. flask run

以上的方法大致类似，flask的自动搜索机制会自动从FLASK_APP的值定义的模块中寻找名称为create_app()或make_app()的工厂函数
## 2. 第三方库
>1. [Bootstrap-Flask](https://bootstrap-flask.readthedocs.io/en/latest/)
>该库是bootstrap4的封装，提供了若干个jinja2函数。
>2. [Flask-login](https://flask-login.readthedocs.io/en/latest/)
>简化用户的登录
## 3. Docker部署
>目前使用到了docker-compose，目前暂时只生成了一个flask容器，flask容器可以通过5000端口访问，该容器并未做端口映射
>nginx负责反向代理，负责转发请求和flask容器，默认绑定80端口。hehe

