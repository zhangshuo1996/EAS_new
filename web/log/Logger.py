import logging
from logging import handlers
import time
import sys
class Logger(object):
    level_relations = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'crit': logging.CRITICAL
    }  # 日志级别关系映射
    # 日志文件格式
    fmt = '%(asctime)s -- %(pathname)s[line:%(lineno)d] -- %(levelname)s: %(message)s'

    def __init__(self, filename, level='info', when='S', backCount=3, fmt=fmt):
        # cur_day = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        # cur_day = time.strftime('%Y-%m-%d-%H-%M', time.localtime(time.time()))
        # print(cur_day)
        # # filename = 'logs/' + filename + "-" + cur_day + ".log"
        # filename = 'logs/' + filename + ".log"
        self.logger = logging.getLogger(filename)
        format_str = logging.Formatter(fmt)  # 设置日志格式
        self.logger.setLevel(self.level_relations.get(level))  # 设置日志级别
        sh = logging.StreamHandler()  # 往屏幕上输出
        sh.setFormatter(format_str)  # 设置屏幕上显示的格式
        th = handlers.TimedRotatingFileHandler(filename=filename, when=when, backupCount=backCount, encoding='utf-8')  # 往文件里写入#指定间隔时间自动生成文件的处理器
        th.setFormatter(format_str)  # 设置文件里写入的格式
        self.logger.addHandler(sh)  # 把对象加到logger里
        self.logger.addHandler(th)

    def combine_msg(self, ip, username, event, message):
        """
        将给定的日志参数组合成字符串
        :return:
        """
        combine_str = ' -- [ip:%(ip)s] -- [username:%(username)s] -' \
                      '- [event:%(event)s] -- [message:%(message)s]' % {"ip": ip, "username": username,
                                                                    "event": event, "message": message
                                                             }
        return combine_str


if __name__ == '__main__':
    while True:

        log = Logger(filename='all4.log', level='debug')
        # log.logger.debug('debug')
        # log.logger.info('info')
        # log.logger.warning('警告')
        # log.logger.error('报错')
        log.logger.critical(log.combine_msg(ip="1.1.1.1", username="none", event="visit_search_page", message="normal"))
        # Logger('normal1.log', levelname='error', ip="1.1.1.1", username="none", event="visit_search_page").logger.info('normal')
        print("--")
        time.sleep(3)