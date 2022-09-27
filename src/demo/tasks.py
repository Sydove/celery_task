# from celery import Celery
#
# app = Celery("tasks", broker='redis://root:123456@47.108.164.71:6379/0',
#              backend='redis://root:123456@47.108.164.71:6379/0')
#
#
# @app.task
# def add(x, y):
#     print(f"开始执行任务：{x},{y}")
#     return x + y
#
