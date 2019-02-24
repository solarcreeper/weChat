#!/usr/bin/python
# -*- coding:utf-8 -*-
import re
import time
import pytz
import datetime
from app.my_logger import logger

RECORD_OK = 0
RECORD_FORMAT_ERROR = 1


def content_parse(collection, content, from_user):
    logger.info("content parse: content is [%s] from_user [%s]" % (content, from_user))
    command = check_format(content)
    if command['error_code'] != RECORD_OK:
        response = u'不支持该命令\r\nr自动记录当前时间: r\r\nu datetime 强制记录指定时间: u 2019-01-01 12:12\r\nq 查询当日记录时间: q\r\nq date 查询指定日期|月份记录时间: q 2019-01-01 | q 2019-01\r\nqa 查询所有记录时间\r\np 查询当日报告\r\np date 查询指定日期|月份报告: q 2019-01-01 | q 2019-01\r\npa 查询所有月份报告'
    else:
        response = get_response(command, collection, from_user)
    return response


def get_response(params, collection, user):
    if params['command'] == '?':
        return u'r 自动记录当前时间: r\r\nu datetime 强制记录指定时间: u 2019-01-01 12:12\r\nq 查询当日记录时间: q\r\nq date 查询指定日期|月份记录时间: q 2019-01-01 | q 2019-01\r\nqa 查询所有记录时间\r\np 查询当日报告\r\np date 查询指定日期|月份报告: q 2019-01-01 | q 2019-01\r\npa 查询所有月份报告'
    if params['command'] == 'r':
        return process_command_r(collection, params['time'], user)
    if params['command'] == 'u':
        return process_command_u(collection, params['time'], user)
    if params['command'] == 'q':
        return process_command_q(collection, params['time'], user)
    if params['command'] == 'qa':
        return process_command_p(collection, params['time'], user)
    if params['command'] == 'p':
        return process_command_p(collection, params['time'], user)
    if params['command'] == 'pa':
        return process_command_p(collection, params['time'], user)


def process_command_r(db_collection, str_time, user):
    if str_time is not None:
        return u'格式错误，{r 自动记录当前时间: r}'
    logger.info("record user: %s time: %s" % (user, str_time))
    current_time = get_time()
    db_collection.save(format_data(user, current_time))
    return u'新增记录：%s' % current_time


def process_command_u(db_collection, str_time, user):
    if is_valid_date_format(str_time, "%Y-%m-%d %H:%M:%S") or is_valid_date_format(str_time, "%Y-%m-%d %H:%M"):
        logger.info("new record: user:%s str_time:%s" % (user, str_time))
        db_collection.save(format_data(user, str_time))
        return u'新增记录：%s' % str_time
    else:
        logger.info("param format error: user:%s str_time:%s" % (user, str_time))
        return u'格式错误\r\n{u datetime 强制记录指定时间: u 2019-01-01 12:12}'


def process_command_q(db_collection, str_time, user):
    if str_time is None:
        str_time = get_time("%Y-%m-%d")
        logger.info("query time is None, reset to %s" % str_time)
    if is_valid_date_format(str_time, "%Y-%m-%d") or is_valid_date_format(str_time, "%Y-%m"):
        logger.info("query record user:%s time:%s" % (user, str_time))
        result = db_collection.find(format_data(user, re.compile(str_time)))
        response = ""
        for r in result:
            response = response + r['time'] + '\r\n'
        logger.info("query result for user:%s time:%s is %s" % (user, str_time, response))
        return response
    else:
        return u'格式错误\r\n{q 查询当日记录时间: q\r\nq date 查询指定日期|月份记录时间: q 2019-01-01 | q 2019-01}'


def process_command_qa(db_collection, str_time, user):
    if str_time is not None:
        return u'格式错误\r\n{qa 查询所有记录时间: qa}'

    result = db_collection.find(format_data(user))
    response = ""
    for r in result:
        response = response + r['time'] + '\r\n'
    logger.info("query result for user:%s time:%s is %s" % (user, str_time, response))
    return response


def process_command_p(db_collection, str_time, user):
    if str_time is None:
        str_time = get_time("%Y-%m-%d")
        logger.info("query time is None, reset to %s" % str_time)
    if not (is_valid_date_format(str_time, "%Y-%m-%d") or is_valid_date_format(str_time, "%Y-%m")):
        return u'格式错误\r\n{q 2019-01-01 | q 2019-01| q}'
    if is_valid_date_format(str_time, "%Y-%m-%d"):
        logger.info("query report for day:%s" % str_time)
        result = db_collection.find(format_data(user, str_time))
        days = []
        for r in result:
            days.append(r['time'])
        if len(days) == 0:
            return u'无当日数据:%s' % str_time
        else:
            early = min(days)

    if is_valid_date_format(str_time, "%Y-%m"):
        logger.info("query report for month:%s" % str_time)


def process_command_pa(collection, str_time, user):
    return 'todo'


def format_data(user, str_time=None):
    if str_time is None:
        return {'user': user}
    else:
        return {'user': user, 'time': str_time}


def get_timestamp(str_time):
    if is_valid_date_format(str_time, "%Y-%m-%d %H:%M"):
        str_time = str_time + ':00'
    time_array = time.strptime(str_time, "%Y-%m-%d %H:%M:%S")
    return time.mktime(time_array)


def get_time_str(timestamp):
    return datetime.datetime.fromtimestamp(timestamp, pytz.timezone('Asia/Chongqing')).strftime('%Y-%m-%d %H:%M:%S')


def check_format(content):
    all_command = ["?", "r", "u", "q", "qa", "p", "pa"]
    input_params = content.split(' ')
    response = dict()
    if input_params[0] not in all_command:
        response['error_code'] = RECORD_FORMAT_ERROR
    else:
        response['command'] = input_params[0]
        if len(input_params) == 1:
            timestr = None
        else:
            timestr = ' '.join(input_params[1:])
        if is_valid_date(timestr):
            response['error_code'] = RECORD_OK
            response['time'] = timestr
        else:
            response['error_code'] = RECORD_FORMAT_ERROR
    return response


def get_time(format_str=None):
    if format_str:
        return datetime.datetime.now(pytz.timezone('Asia/Chongqing')).strftime(format_str)
    else:
        return datetime.datetime.now(pytz.timezone('Asia/Chongqing')).strftime("%Y-%m-%d %H:%M")


def is_valid_date_format(str_date, format_str):
    try:
        time.strptime(str_date, format_str)
        return True
    except Exception as e:
        print(e)
        return False


def is_valid_date(str_date):
    if str_date is None:
        return True
    try:
        if ":" in str_date:
            if str_date.count(":") == 2:
                time.strptime(str_date, "%Y-%m-%d %H:%M:%S")
            else:
                time.strptime(str_date, "%Y-%m-%d %H:%M")
        else:
            if str_date.count('-') == 2:
                time.strptime(str_date, "%Y-%m-%d")
            else:
                time.strptime(str_date, "%Y-%m")
        return True
    except Exception as e:
        print(e)
        return False


def test():
    time1 = get_timestamp('2019-02-23 10:12')
    time2 = datetime.datetime.fromtimestamp(time1, pytz.timezone('Asia/Chongqing')).strftime('%Y-%m-%d %H:%M:%S')

    pass


if __name__ == '__main__':
    test()
    from app.views import db

    collection = db.test
    collection.drop()
    from_user = 'test'
    test_command = [
        '?',
        'r',
        'q',
        'u 2019-02-23 10:12',
        # 'u 2019-02-23 10:12',
        # 'q 2019-02',
        # 'q 2019-02-23',
        # 'p',
        # 'pa',
    ]
    for c in test_command:
        print(content_parse(collection, c, from_user))
