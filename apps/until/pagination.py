#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author  : hu_cl
# @Contact : 760730895@qq.com 
# @Date    : 2020/12/10 16:33
# @File    : pagination.py
from rest_framework.response import Response
from collections import OrderedDict
from rest_framework.pagination import PageNumberPagination
from django.core.paginator import Paginator
from django.utils.functional import cached_property


class FasterDjangoPaginator(Paginator):
    @cached_property
    def count(self):
        # only select 'id' for counting, much cheaper
        return self.object_list.values('id').count()


class MyPagination(PageNumberPagination):
    django_paginator_class = FasterDjangoPaginator

    page_size = 10  # 每页显示多少条
    page_size_query_param = 'page_size'  # URL中每页显示条数的参数
    page_query_param = 'page'  # URL中页码的参数
    max_page_size = 100  # 前端最多能设置的每页数量

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('results', data)
        ]))
