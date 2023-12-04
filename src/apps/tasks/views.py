# -*- coding: UTF-8 -*-
"""
@Author : Sydove
@Project ：celery_task
@Time : 2023/2/9 16:30
@File : views.py.py
@attention:
"""
import json

from django.views import View
from django.http import JsonResponse
from models.models import User, Store
from django.db import transaction


class Task(View):

    def get(self, request):
        data = User.objects.all()
        result = [{"name": item.name} for item in data]
        return JsonResponse(result,safe=False)


    def post(self, request):
        """
        测试事务
        """
        print("")
        json_data = request.body.decode('utf-8')

        # 解析 JSON 数据
        try:
            with transaction.atomic():
                data = json.loads(json_data)
                index = data["data"]
                name = f"name_{index}"
                user = User.objects.create(name=name)
                # raise Exception("error")
                Store.objects.create(name=name, user=user)
                return JsonResponse({"code": 200, "msg": "Success", "data": {}})
        except Exception as e:
            return JsonResponse({"code": 500, "msg": "Success", "data": {}})

