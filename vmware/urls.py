# -*- coding: utf-8 -*-

#from django.conf.urls import patterns
from django.urls import path,include
from django.shortcuts import render
from .views import *
app_name="vmware"

def index(request):
    return render(request, 'index.html')    

urlpatterns = (
    #path('', index),
    path('', home),
    path('vminfo',getvminfo),	
    path('webmks/',webmks),	#webconsole
    path('input',vminfo_input),	#触发获取虚拟机列表，并更新数据库-----------get
    #power control VM
    path('poweronvm',poweronvm),
    path('poweroffvm',poweroffvm),
    #Just for test
    path('test',testurl),
)
