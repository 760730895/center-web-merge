# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# Author     ：hu_cl
# Date       ：2022/3/22 10:51
# File       : urls.py
# Description：
"""
from django.conf.urls import url, include
from apps.register import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('operate', views.OperatingViewSet, basename='系统操作')
router.register('info', views.ConfigAddressViewSet, basename='本地配置信息')
router.register('sub', views.RegisterSubInfoViewSet, basename='sub注册api')
router.register('sup', views.RegisterSupInfoViewSet, basename='sup注册api')

urlpatterns = [
    url(r'^', include(router.urls)),
]
