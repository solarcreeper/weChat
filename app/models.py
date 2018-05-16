#!/usr/bin/python
# -*- coding:utf-8 -*-
import time

from .my_logger import logger


def content_parse(collection, content, from_user):
    logger.info("content parse: content is [%s] from_user [%s]" % (content, from_user))
    ckeck, parser_result = check_content(content)
    if not ckeck:
        return parser_result

    record_templete = {'user': from_user, 'timestamp': time.strftime("%Y-%m-%d", time.localtime())}
    if parser_result[0] in ['q', 'r']:
        content = run_qr(collection, parser_result, record_templete)
    else:
        content = run_upadte(collection, parser_result, record_templete)
    return content


def run_qr(collection, parser, record_templete):
    record = collection.find_one(record_templete)
    if parser[0] == 'r':
        collection.remove(record)
        content = u'删除记录【%s】' % record
    else:
        content = u'查询结果【%s】' % record
    return content


def run_upadte(collection, parser, record_templete):
    record = collection.find_one(record_templete)
    if record is None:
        record = record_templete
    record.update(_list2dict(parser))
    collection.save(record)
    return u'更新记录【%s】' % record


def check_content(content):
    logger.info("check content: content is [%s]" % content)
    allowed_record = ['bike', 'flat', 'situp']
    parser = content.split(' ')
    if parser[0].lower() != 'record' or len(parser) < 2:
        logger.info("input command start with [%s] and input command length is [%s]" % (parser[0], len(parser)))
        return False, u'使用{record bike|situp|flat num} or {record q|r}格式进行记录'

    ckeck = True
    parser_result = None
    if len(parser) == 2:
        if parser[1] in ['q', 'r']:
            logger.info("input command is [%s]" % parser[1])
            parser_result = parser[1:]
        else:
            logger.info("invalid command [%s]" % content)
            parser_result = u'使用{record bike|situp|flat num} or {record q|r}格式进行记录'
            ckeck = False
    else:
        if len(parser) % 2 == 1:
            i = 1
            parser_result = parser[1:]
            while i < len(parser):
                if parser[i] not in allowed_record:
                    logger.info("invalid value [%s] in command [%s]" % (parser[i], content))
                    parser_result = u'使用{record bike|situp|flat num} or {record q|r}格式进行记录'
                    ckeck = False
                    break
                elif not _str2digital(parser[i+1]):
                    logger.info("invalid value [%s] in command [%s]" % (parser[i], content))
                    parser_result = u'使用{record bike|situp|flat num} or {record q|r}格式进行记录'
                    ckeck = False
                    break
                else:
                    i = i + 2
        else:
            logger.info("input command error")
            parser_result = u'使用{record bike|situp|flat num} or {record q|r}格式进行记录'
            ckeck = False
    return ckeck, parser_result


def _list2dict(l):
    i = 0
    data = {}
    while i < len(l):
        data[l[i]] = l[i + 1]
        i = i + 2
    return data


def _str2digital(str):
    if str.isdigit():
        return True
    try:
        float(str)
        return True
    except ValueError:
        return False


