#!/usr/bin/python
# -*- coding:utf-8 -*-
import time


def content_parse(collection, content, from_user):
    parser = content.split(' ')
    if parser[0] != 'record' or len(parser) < 2 or len(parser) % 2 != 1:
        content = "暂不支持此操作"
    else:
        i = 1
        data = {}
        while(i < len(parser)):
            data[parser[i]] = parser[i+1]
            i = i + 2
        content = "记录完成"
        record_templete = {'user': from_user, 'timestamp':  time.strftime("%Y-%m-%d", time.localtime())}
        record = collection.find_one(record_templete)
        if record is None:
            record = record_templete
        if 'bike' in data:
            record['bike'] = data['bike']
        if 'flat' in parser:
            record['flat'] = data['flat']
        if 'situp' in parser:
            record['situp'] = data['situp']
        obj_id = collection.save(record)
    return content