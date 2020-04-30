import logging
import logstash
# from logstash import AMQPLogstashHandler
import sys

if __name__ == '__main__':
    # host为logstash的IP地址
    # host = '47.102.113.60'
    host = '39.100.224.138'

    test_logger = logging.getLogger('python-logstash-logger')
    test_logger.setLevel(logging.INFO)
    # 创建一个ogHandler
    test_logger.addHandler(logstash.LogstashHandler(host, 5005, version=1))
    # test_logger.addHandler(logstash.AMQPLogstashHandler(version=1,
    #                                                     host=host, durable=True, username="elastic", password="elk2020"))

    test_logger.error('这是一行测试日志')
    test_logger.info('python-logstash: test logstash info message.')
    test_logger.warning('python-logstash: test logstash warning message.')
    print("--------")