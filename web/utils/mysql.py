import pymysql
import logging
from pymysql import cursors
from flask import _app_ctx_stack, current_app


class MySQL(object):
    def __init__(self, app=None):
        self.app = app
        # 事务数，支持嵌套
        self.transactions = 0
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """Initialize the `app` for use with this
        """
        app.config.setdefault('MYSQL_HOST', 'localhost')
        app.config.setdefault('MYSQL_USER', None)
        app.config.setdefault('MYSQL_PASSWORD', None)
        app.config.setdefault('MYSQL_DB', None)
        app.config.setdefault('MYSQL_PORT', 3306)
        app.config.setdefault('MYSQL_UNIX_SOCKET', None)
        app.config.setdefault('MYSQL_CONNECT_TIMEOUT', 10)
        app.config.setdefault('MYSQL_READ_DEFAULT_FILE', None)
        app.config.setdefault('MYSQL_USE_UNICODE', True)
        app.config.setdefault('MYSQL_CHARSET', 'utf8')
        app.config.setdefault('MYSQL_SQL_MODE', None)
        app.config.setdefault('MYSQL_CURSORCLASS', None)

        if hasattr(app, 'teardown_appcontext'):
            app.teardown_appcontext(self.teardown)

    @property
    def connect(self):
        kwargs = {}

        if current_app.config['MYSQL_HOST']:
            kwargs['host'] = current_app.config['MYSQL_HOST']

        if current_app.config['MYSQL_USER']:
            kwargs['user'] = current_app.config['MYSQL_USER']

        if current_app.config['MYSQL_PASSWORD']:
            kwargs['passwd'] = current_app.config['MYSQL_PASSWORD']

        if current_app.config['MYSQL_DB']:
            kwargs['db'] = current_app.config['MYSQL_DB']

        if current_app.config['MYSQL_PORT']:
            kwargs['port'] = current_app.config['MYSQL_PORT']

        if current_app.config['MYSQL_UNIX_SOCKET']:
            kwargs['unix_socket'] = current_app.config['MYSQL_UNIX_SOCKET']

        if current_app.config['MYSQL_CONNECT_TIMEOUT']:
            kwargs['connect_timeout'] = \
                current_app.config['MYSQL_CONNECT_TIMEOUT']

        if current_app.config['MYSQL_READ_DEFAULT_FILE']:
            kwargs['read_default_file'] = \
                current_app.config['MYSQL_READ_DEFAULT_FILE']

        if current_app.config['MYSQL_USE_UNICODE']:
            kwargs['use_unicode'] = current_app.config['MYSQL_USE_UNICODE']

        if current_app.config['MYSQL_CHARSET']:
            kwargs['charset'] = current_app.config['MYSQL_CHARSET']

        if current_app.config['MYSQL_SQL_MODE']:
            kwargs['sql_mode'] = current_app.config['MYSQL_SQL_MODE']

        if current_app.config['MYSQL_CURSORCLASS']:
            kwargs['cursorclass'] = getattr(cursors, current_app.config['MYSQL_CURSORCLASS'])

        return pymysql.connect(**kwargs)

    @property
    def connection(self):
        """Attempts to connect to the MySQL server.
        :return: Bound MySQL connection object if successful or ``None`` if
            unsuccessful.
        """

        ctx = _app_ctx_stack.top
        if ctx is not None:
            if not hasattr(ctx, 'mysql_db'):
                ctx.mysql_db = self.connect
            return ctx.mysql_db

    def __enter__(self):
        self.transactions = self.transactions + 1
        logging.info('begin transaction...' if self.transactions == 1 else 'join current transaction...')
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        """支持事务，支持事务提交和回滚"""
        self.transactions = self.transactions - 1
        try:
            if self.transactions == 0:
                if exc_type is None:
                    self.connection.commit()
                    logging.info('end transaction, commit...')
                else:
                    self.connection.rollback()
                    logging.info('end transaction, rollback...')
        finally:
            pass

    def teardown(self, exception):
        ctx = _app_ctx_stack.top
        if hasattr(ctx, 'mysql_db'):
            ctx.mysql_db.close()

    def _select(self, sql, first, *args):
        """
        select语句
        :param sql: SQL语句 内部变量使用?
        :param first: 是否只获取一个
        :param args: SQL语句中要使用的变量
        :return: 返回查询的结果
        """
        cursor = None
        logging.info('SQL: %s %s' % (sql, args if len(args) > 0 else ""))
        sql = sql.replace('?', '%s')

        try:
            connection = self.connection
            cursor = connection.cursor(cursor=pymysql.cursors.DictCursor)
            # 利用本身的 execute 函数的特性，传入两个参数：sql语句与tuple类型的参数，以避免sql注入
            cursor.execute(sql, args)

            if first:
                result = cursor.fetchone()
                return result
            else:
                results = cursor.fetchall()
                return results
        except Exception as e:
            print(e)
            return None
        finally:
            cursor.close()
            # connection.close()

    def select_one(self, sql, *args):
        """
        执行select SQL语句并返回dict结构的结果或None
        :param sql:select的SQL语句，包含?
        :param args:select的SQL语句所对应的值
        :return: dict结构的一个结果或者None
        """
        return self._select(sql, True, *args)

    def select(self, sql, *args):
        """
        执行SQL语句
        :param sql:  select的SQL语句，可含?
        :param args: select的SQL语句所对应的值
        :return: list(dict) 或者None
        """
        return self._select(sql, False, *args)

    def _insert(self, sql, insert_many, *args):
        """
        insert语句
        :param sql: SQL语句 内部变量使用?
        :param insert_many: 是否要插入多行
        :param args: SQL语句中要使用的变量
        :return: 返回插入的结果 插入失败则返回-1
        """
        connection = None
        cursor = None
        logging.info('SQL: %s %s' % (sql, args if len(args) > 0 else ""))
        sql = sql.replace('?', '%s')
        try:
            connection = self.connection
            cursor = connection.cursor(cursor=pymysql.cursors.DictCursor)

            # 利用本身的 execute 函数的特性，传入两个参数：sql语句与tuple类型的参数，以避免sql注入
            if insert_many:
                # 插入多行
                cursor.executemany(sql, args)
            else:
                cursor.execute(sql, args)
            # 返回最后插入行的主键ID
            if self.transactions == 0:
                logging.info('auto commit')
                connection.commit()
            return cursor.lastrowid
        except Exception as e:
            print(e)
            connection.rollback()  # 事务回滚
        finally:
            cursor.close()
            # connection.close()
        return -1

    def insert(self, sql, *args):
        """
        执行SQL语句
        :param sql:  insert的SQL语句，可含?
        :param args: insert的SQL语句所对应的值
        :return: 最后插入行的主键ID 如果插入失败返回-1
        """
        return self._insert(sql, False, *args)

    def insert_many(self, sql, *args):
        """
        执行SQL语句
        :param sql:  insert的SQL语句，可含?
        :param args: insert的SQL语句所对应的值
        :return: 最后插入行的主键ID
        """
        return self._insert(sql, True, *args)

    def _update(self, sql, *args):
        """
        select语句
        :param sql: SQL语句 内部变量使用?
        :param args: SQL语句中要使用的变量
        :return: 返回操作的行数
        """
        connection = None
        cursor = None
        logging.info('SQL: %s %s' % (sql, args if len(args) > 0 else ""))
        sql = sql.replace('?', '%s')
        row_count = 0
        try:
            connection = self.connection
            cursor = connection.cursor(cursor=pymysql.cursors.DictCursor)
            # 利用本身的 execute 函数的特性，传入两个参数：sql语句与tuple类型的参数，以避免sql注入
            cursor.execute(sql, args)
            # 获取影响的行
            row_count = cursor.rowcount
            if self.transactions == 0:
                logging.info('auto commit')
                connection.commit()
        except Exception as e:
            connection.rollback()
            print("db operation error is : ", e)
            return False
        finally:
            cursor.close()
            # connection.close()
        return row_count

    def update(self, sql, *args):
        """
        执行SQL语句
        :param sql:  SQL语句，可含?
        :param args: delete的SQL语句所对应的值
        :return: 返回受影响的行数
        """
        return self._update(sql, *args)

    def delete(self, sql, *args):
        """
        执行SQL语句
        :param sql:  SQL语句，可含?
        :param args: select的SQL语句所对应的值
        :return: 1或-1
        """
        return self._delete(sql, *args)

    def _delete(self, sql, *args):
        """
         delete语句
        :param sql: SQL语句 内部变量使用?
        :param args: SQL语句中要使用的变量
        :return: 返回
        """
        connection = None
        cursor = None
        logging.info('SQL: %s %s' % (sql, args if len(args) > 0 else ""))
        sql = sql.replace('?', '%s')
        try:
            connection = self.connection
            cursor = connection.cursor(cursor=pymysql.cursors.DictCursor)
            # 利用本身的 execute 函数的特性，传入两个参数：sql语句与tuple类型的参数，以避免sql注入
            cursor.execute(sql, args)
            # 获取影响的行
            row_count = cursor.rowcount
            if self.transactions == 0:
                logging.info('auto commit')
                connection.commit()
        except Exception as e:
            connection.rollback()
            print("db operation error is : ", e)
            return -1
        finally:
            cursor.close()
            # connection.close()
        return row_count
