#!/usr/bin/python
# -*- coding:utf-8 -*-
import time


def content_parse(collection, content, from_user):
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
    record.update(list2dict(parser))
    collection.save(record)
    return u'更新记录【%s】' % record


def check_content(content):
    allowed_record = ['bike', 'flat', 'situp']
    parser = content.split(' ')
    if parser[0].lower() != 'record' or len(parser) < 2:
        return False, u'使用{record bike|situp|flat num} or {record q|r}格式进行记录'

    ckeck = True
    parser_result = None
    if len(parser) == 2:
        if parser[1] in ['q', 'r']:
            parser_result = parser[1:]
        else:
            parser_result = u'使用{record bike|situp|flat num} or {record q|r}格式进行记录'
            ckeck = False
    else:
        if len(parser) % 2 == 1:
            i = 1
            parser_result = parser[1:]
            while i < len(parser):
                if parser[i] not in allowed_record:
                    parser_result = u'使用{record bike|situp|flat num} or {record q|r}格式进行记录'
                    ckeck = False
                    break
                else:
                    i = i + 2
        else:
            parser_result = u'使用{record bike|situp|flat num} or {record q|r}格式进行记录'
            ckeck = False
    return ckeck, parser_result


def list2dict(l):
    i = 0
    data = {}
    while i < len(l):
        data[l[i]] = l[i + 1]
        i = i + 2
    return data
