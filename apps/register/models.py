from django.db import models


# Create your models here.

class RegisterSupInfo(models.Model):
    id = models.BigAutoField(primary_key=True)
    ip = models.GenericIPAddressField()
    register_pw = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    pid = models.CharField(max_length=255)
    time = models.DateTimeField(blank=True, null=True)
    des = models.CharField(max_length=255, blank=True, null=True)
    user_id = models.IntegerField()
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    role = models.SmallIntegerField()

    class Meta:
        managed = True
        db_table = 'register_sup_info'


class RegisterSubInfo(models.Model):
    id = models.SmallAutoField(primary_key=True)
    sid = models.CharField('节点id', max_length=255)
    pid = models.CharField('节点上级id', max_length=255)
    ip = models.GenericIPAddressField()
    type = models.SmallIntegerField('1-yihnac|2-manager')
    username = models.CharField('为pid提供的用户', max_length=255)
    password = models.CharField('用户对应的密码', max_length=255)
    role = models.SmallIntegerField('用户对应的权值')
    location = models.CharField('行政地区', max_length=255, blank=True, null=True)
    net_name = models.CharField('网络名称', max_length=255, blank=True, null=True)
    des = models.CharField('说明', max_length=255, blank=True, null=True)
    time = models.DateTimeField('注册时间', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'register_sub_info'


class ConfigAddress(models.Model):
    id = models.SmallAutoField(primary_key=True)
    local_ip = models.GenericIPAddressField()
    netmask = models.CharField('子网掩码', max_length=255)
    gateway = models.CharField('网关地址', max_length=255)
    location = models.CharField('本级平台名称', max_length=255)
    loc_des = models.CharField('本级平台描述', max_length=255)

    class Meta:
        managed = True
        db_table = 'config_address'
