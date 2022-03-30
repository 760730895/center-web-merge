# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# Author     ：hu_cl
# Date       ：2022/3/24 9:58
# File       : mg_config.py.py
# Description：系统所需要的全局变量
"""
import uuid

# 手动填写唯一标识
owner_uid = None
# 自动生成唯一标识
owner_id = uuid.uuid1().hex[-12:] if not owner_uid else owner_uid

# http://192.168.2.235:8080/CyApi/system/user/info/
def add_url(ip, api_path, port=8090):
    add_url = "http://{}:{}{}".format(ip, port, api_path)
    return add_url
