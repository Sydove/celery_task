FROM python:3.7.5

WORKDIR /root/celery_task

ADD ./requirements.txt /root/celery_task

RUN pip install -r requirements.txt -i https://pypi.douban.com/simple/