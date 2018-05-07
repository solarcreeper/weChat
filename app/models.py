#!/usr/bin/python
# -*- coding:utf-8 -*-
import time


def content_parse(collection, content, from_user):
    ckeck, ckeck_reply, parsed_record, parsed_not_allowd_record = check_content(content)
    if not ckeck:
        content = ckeck_reply
        return content

    record_templete = {'user': from_user, 'timestamp': time.strftime("%Y-%m-%d", time.localtime())}
    if len(parsed_record) == 1:
        content = run_qr(collection, parsed_record, record_templete)
    else:
        content = run_upadte(collection, parsed_record, record_templete)

    if len(parsed_not_allowd_record) > 0:
        content = content + u'以下数据格式不正确【%s】' % str(parsed_not_allowd_record)
    return content

def run_qr(collection, parser,record_templete):
    record = collection.find_one(record_templete)
    if parser[0] == 'r':
        collection.remove(record)
        content = u'删除记录【%s】' %record
    else:
        content = u'查询结果【%s】' %record
    return content

def run_upadte(collection, parser, record_templete):
    record = collection.find_one(record_templete)
    record.update(parser)
    return u'更新记录【%s】' %record

def check_content(content):
    parser = content.split(' ')
    ckeck_reply = None
    if parser[0].lower() != 'record':
        ckeck_reply = u'使用record bike|situp|flat num 格式进行记录'
        ckeck = False
    elif len(parser) == 2 and (parser[1] != 'q' or parser[1] != 'r'):
        ckeck_reply = u'格式不正确，目前只支持{record q|r}and {record bike|situp|flat num}操作'
        ckeck = False
    elif len(parser) < 2:
        ckeck_reply = u'格式不正确，目前只支持record q|r 操作'
        ckeck = False
    elif len(parser) > 2 and len(parser) % 2 == 0:
        ckeck_reply = u'格式不正确，目前只支持{record q|r}and {record bike|situp|flat num}操作'
        ckeck = False
    else:
        ckeck = True

    if ckeck:
        allowed_record = ['bike', 'flat', 'situp']
        record = {}
        not_allowed_record = {}
        i = 1
        while (i < len(parser)):
            if parser[i] in allowed_record:
                record[parser[i]] = parser[i + 1]
            else:
                not_allowed_record[parser[i]] = parser[i+1]
            i = i + 2
        if len(record) == 0:
            ckeck_reply = u'使用record bike|situp|flat num 格式进行记录'
            ckeck = False
    else:
        record = None
        not_allowed_record = None
    return ckeck, ckeck_reply, record, not_allowed_record