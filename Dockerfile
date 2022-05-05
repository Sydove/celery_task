FROM python:3.7.5

WORKDIR /root/yuncong_service

ADD ./requirements.txt /root/yuncong_service

RUN pip install -r requirements.txt -i https://pypi.douban.com/simple/