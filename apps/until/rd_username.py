# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# Author     ：hu_cl
# Date       ：2022/3/23 14:30
# File       : rd_username.py
# Description：
"""
import random

from django.db.models import Max

from apps.register import models


def register_create_user(id, len):
    # 8位用户名
    items = models.RegisterSubInfo.objects.all()
    max_role = items.aggregate(Max('role'))
    while True:
        username = ''.join(
            random.sample("1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ", len))
        if items.filter(username=username).exists():
            continue
        else:
            break
    num = 0 if not max_role['role__max'] else int(max_role['role__max'])
    return {"username": username, "password": "YiHNAC@123", "role": num + 1}


def register_delete_user(id):
    try:
        items = models.RegisterSubInfo.objects.all()
        delete_item = items.filter(id=id).delete()
        code = 1
    except Exception as ex:
        print('删除用户错误', ex)
        code = 0

    return code
