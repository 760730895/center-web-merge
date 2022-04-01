import datetime
import hashlib

# Create your views here.
import os
import threading
import time

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.settings import api_settings

from apps.register import models, serializers
from apps.until.api_method import url_post_api, url_delete_api
from apps.until.rd_username import register_create_user
from nacc_manager.mg_config import add_url, owner_id


class ConfigAddressViewSet(viewsets.ModelViewSet):
    queryset = models.ConfigAddress.objects.all()
    serializer_class = serializers.ConfigAddressSerializer
    ordering = ('id',)

    def list(self, request, *args, **kwargs):
        queryset = self.queryset.first()
        serializer = self.get_serializer(queryset)
        return Response(serializer.data)


class OperatingViewSet(viewsets.GenericViewSet):
    @classmethod
    def oper_sys(self, data):
        if data in ['reboot', 'shutdown']:
            time.sleep(5)

        os.system(data)

    @action(methods=['post'], detail=False)
    def methods(self, request, *args, **kwargs):
        if request.data['operate'] in ['reboot', 'shutdown']:
            thread = threading.Thread(target=self.oper_sys, args=(request.data['operate'],))
            thread.start()
            return Response('执行成功', status=status.HTTP_200_OK)
        else:
            return Response('输入参数不对', status=status.HTTP_400_BAD_REQUEST)


class RegisterSubInfoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.RegisterSubInfo.objects.all()
    serializer_class = serializers.RegisterSubInfoSerializer
    ordering = ('id',)

    def perform_create(self, serializer):
        serializer.save()

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}

    @action(methods=['get'], detail=False, permission_classes=[], url_name='register_query_sub')
    def register_query_sub(self, request, pk=None):
        """
        调用：上级调用
        说明：查询直接下级manager的注册信息表
        方式：get
        参数：id，调用者的id
        返回：{[{},{}]}
        实现：查询register_sub_info，将其返回
        :param request:
        :param pk:
        :return:
        """
        queryset = self.get_queryset().filter(sid=request.query_params['sid'])
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['post'], detail=False, permission_classes=[], url_name='register_recv')
    def register_recv(self, request, pk=None):
        auth = hashlib.md5((owner_id + request.data['password']).encode("utf-8")).hexdigest()
        if request.data['auth'] != auth:
            return Response('特征码 err', status=status.HTTP_401_UNAUTHORIZED)
        data = request.data.copy()
        data['pid'] = owner_id
        data['net_name'] = None
        data['des'] = None
        data['time'] = datetime.datetime.now()
        if self.queryset.filter(sid=data['sid'], pid=owner_id).exists():
            return Response('系统已经注册,需先取消注册才能注册', status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(methods=['delete'], detail=False, permission_classes=[], url_name='register_delete')
    def register_delete(self, request, pk=None):
        """
        调用：下级调用
        说明：为下级提供的取消注册的api
        参数：id，取消注册者的id
        """
        pk = request.query_params['sid']
        for item in self.queryset.filter(sid=pk):
            down_url = add_url(item.ip, api_path=f'/system/user/delete_user/?uid={owner_id}', port=8090)
            code1, data1, msg1 = url_delete_api(down_url)
            if code1 >= 400:
                return Response(f'delete_user1 api err:{msg1}', status=status.HTTP_408_REQUEST_TIMEOUT)
        for it in self.queryset.filter(pid=pk):
            down_url = add_url(it.ip, api_path=f'/system/user/delete_user/?uid={owner_id}', port=8090)
            code2, data2, msg2 = url_delete_api(down_url)
            if code2 >= 400:
                return Response(f'delete_user2 api err:{msg2}', status=status.HTTP_408_REQUEST_TIMEOUT)

        local_up_item = models.RegisterSupInfo.objects.all().first()
        if local_up_item:
            up_url = add_url(local_up_item.ip, api_path=f'/register/sub/register_delete/?sid={local_up_item.pid}',
                             port=8008)
            code3, data3, msg3 = url_delete_api(up_url)
            if code3 != 200:
                return Response(f'register_delete3 api err:{msg3}', status=status.HTTP_408_REQUEST_TIMEOUT)
        self.queryset.filter(sid=pk).delete()
        self.queryset.filter(pid=pk).delete()
        return Response('上级取消注册api成功', status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False, permission_classes=[], url_name='own_uid')
    def own_uid(self, request, pk=None):
        data = owner_id
        return Response(data, status=status.HTTP_200_OK)


class RegisterSupInfoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.RegisterSupInfo.objects.all()
    serializer_class = serializers.RegisterSupInfoSerializer
    ordering = ('id',)

    def list(self, request, *args, **kwargs):
        queryset = self.queryset.first()
        serializer = self.get_serializer(queryset)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save()

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}

    @action(methods=['post'], detail=False, permission_classes=[], url_name='register_up')
    def register_up(self, request, pk=None):
        """
        :des 向上级注册api，调用yihnac的api创建user，组织好此参数，调用上级manager的recv_register
        :request.data 请求参数 {'ip':'','password':'','location':'','user_id':''}
        """
        local_items = models.ConfigAddress.objects.all().first()
        pid = request.data['user_id']
        if self.queryset.filter(pid=pid).exists():
            """取消注册，然后注册"""
            return Response('系统已经注册,需先取消注册才能注册', status=status.HTTP_403_FORBIDDEN)
        else:
            """第一次注册"""
            data = register_create_user(pid, 6)
            # {"username": username, "password": "YiHNAC@123", "role": max_role}
            data['ip'] = request.data['ip']
            data['register_pw'] = request.data['password'] if 'password' in request.data.items() else None
            data['location'] = local_items.location
            data['pid'] = pid
            data['time'] = datetime.datetime.now()
            data['des'] = local_items.loc_des
            data['user_id'] = 0
            try:
                # 调用creat_user api
                url = add_url('127.0.0.1', api_path='/system/user/create_user/', port=8090)
                create_up_body = {
                    "username": data['username'],
                    "password": data['password'],
                    "is_active": True,
                    "is_superuser": True,
                    "show_pw": "YiHNAC@123",
                    "uid": pid,
                    "power": data['role']
                }
                code1, result1, msg1 = url_post_api(url, create_up_body)
                if code1 >= 400:
                    return Response(f'请求creat_user api err:{msg1}', status=status.HTTP_412_PRECONDITION_FAILED)
                # 调用上级的register_recv\
                up_url = add_url(data['ip'], api_path='/register/sub/register_recv/', port=8008)
                register_recv_body = {
                    "ip": local_items.local_ip,
                    "location": data['location'],
                    "net_name": None,
                    "sid": owner_id,
                    "type": 2,
                    "username": data['username'],
                    "password": data['password'],
                    "role": data['role'],
                    "auth": hashlib.md5((pid + data['password']).encode("utf-8")).hexdigest()
                }
                code2, result2, msg2 = url_post_api(up_url, register_recv_body)
                if code2 >= 400:
                    owner_url = add_url('127.0.0.1', api_path=f'/system/user/delete_user/?uid={pid}', port=8090)
                    code, data, msg = url_delete_api(owner_url)
                    return Response(f'register_recv api err:{msg2}', status=status.HTTP_412_PRECONDITION_FAILED)
            except Exception as exp:
                owner_url = add_url('127.0.0.1', api_path=f'/system/user/delete_user/?uid={pid}', port=8090)
                code, data, msg = url_delete_api(owner_url)
                return Response(exp, status=status.HTTP_400_BAD_REQUEST)

            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(methods=['delete'], detail=False, permission_classes=[], url_name='register_un')
    def register_un(self, request, pk=None):
        """
        yihnac取消注册的时候需要调用
        :param request:
        :param pk:
        :return:
        """
        pid = request.query_params['pid']
        owner_url = add_url('127.0.0.1', api_path=f'/system/user/delete_user/?uid={pid}', port=8090)
        code1, data1, msg1 = url_delete_api(owner_url)
        if code1 >= 400:
            return Response(f'delete_user api err,{msg1}', status=status.HTTP_408_REQUEST_TIMEOUT)
        if self.queryset.filter(pid=pid).exists():
            up_items = self.queryset.get(pid=pid)
            up_ip = up_items.ip
            up_url = add_url(up_ip, api_path=f'/register/sub/register_delete/?sid={owner_id}', port=8008)
            code2, data2, msg2 = url_delete_api(up_url)
            if code2 >= 400:
                return Response(f'register_delete api err:{msg2}', status=status.HTTP_408_REQUEST_TIMEOUT)
            self.queryset.filter(pid=pid).delete()

        return Response('取消注册成功', status=status.HTTP_204_NO_CONTENT)

    @action(methods=['post'], detail=False, permission_classes=[], url_name='push_message')
    def push_message(self, request, pk=None):
        """
        说明：下级向上级推送数据
        方式：post
        参数：json格式 {“id”:  “”, “message_type”: “数据类型”, “content”: “”}
        实现：
        1.收到下级的数据，处理
        2.调用直接上级的push_message，转发给上级
        参数说明：
        id：发送该数据的节点的id
        message_type：自定义的数据类型。
        content：内容
        :param request:
        :param pk:
        :return:
        """
        data = request.data.deepcopy()
        pass
        return Response(status=status.HTTP_200_OK)