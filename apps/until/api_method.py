# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# Author     ：hu_cl
# Date       ：2022/3/23 15:47
# File       : api_method.py
# Description：调用外部接口数据
"""
import json
import requests

timeout = (10, 5)


def url_post_api(url, body):
    """
    调用外部api接口
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
        'Content-Type': 'application/json'
    }
    api_json = json.dumps(body)
    print('************url_post_api*********\n', url, '\n', api_json)
    api_data = requests.post(url=url, headers=headers, data=api_json, timeout=timeout)
    api_info = json.loads(api_data.text)
    api_code = api_info["code"]
    api_result = api_info['data']
    api_msg = api_info['msg']
    print(api_code, '\n', api_result, '\n', api_msg, '************url_post_api*********\n')

    return api_code, api_result, api_msg


def url_delete_api(url):
    """
        调用外部api接口
        """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
        'Content-Type': 'application/json'
    }
    print('*********url_delete_api************\n', url)
    api_data = requests.delete(url, headers=headers, timeout=timeout)
    api_info = json.loads(api_data.text)
    api_code = api_info["code"]
    api_result = api_info['data']
    api_msg = api_info['msg']
    print(api_code, '\n', api_result, '\n', api_msg, '**********url_delete_api***********\n')

    return api_code, api_result, api_msg


def url_get_api(url):
    """
        调用外部api接口
        """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
        'Content-Type': 'application/json'
    }
    print('**************url_get_api*************\n', url)
    api_data = requests.get(url, headers=headers, timeout=timeout)
    api_info = json.loads(api_data.text)
    api_code = api_info["code"]
    api_result = api_info['data']
    api_msg = api_info['msg']
    print(api_code, '\n', api_result, '\n', api_msg, '**************url_get_api***********\n')

    return api_code, api_result, api_msg
