from django.urls import path,include
from django.shortcuts import render
from .views import *
app_name="sshmonitor"

def index(request):
	return render(request, 'index.html')	

urlpatterns = [
    path('', index),
]
