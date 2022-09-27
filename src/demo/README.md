# Celery Demo
### 启动celery命令
```shell
celery -A tasks worker --loglevel=info
```
启动之后执行`producer.py`文件，生产任务。