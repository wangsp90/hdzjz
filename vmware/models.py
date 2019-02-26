# -*- coding: utf-8 -*-
from django.db import models

#虚拟机基础信息表
class vminfo(models.Model):
	ID=models.AutoField(primary_key=True)
	VMNAME=models.CharField(max_length=200,null=False)
	IPADDRESS=models.CharField(max_length=100,null=True)
	USER=models.CharField(max_length=100,null=True)
	OS=models.CharField(max_length=100,null=True)
	INSTANCEUUID=models.CharField(max_length=100,null=True)