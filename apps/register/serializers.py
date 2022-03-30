#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author  : hu_cl
# @Email   : hucl91@qq.com
# @Date    : 2021/10/25 15:32
# @File    : serializers.py
# @Disc    :
from rest_framework import serializers
from apps.register import models


# 类名定为表名称 + Serializer

class RegisterSupInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RegisterSupInfo
        fields = '__all__'


class RegisterSubInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RegisterSubInfo
        fields = '__all__'


class ConfigAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ConfigAddress
        fields = '__all__'
