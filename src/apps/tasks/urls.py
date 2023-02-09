# -*- coding: UTF-8 -*-
"""
@Author : Sydove
@Project ：celery_task 
@Time : 2023/2/9 16:31 
@File : urls.py
@attention:
"""
from django.urls import path
from apps.tasks import views


urlpatterns = [
    path("",views.Task.as_view())
]