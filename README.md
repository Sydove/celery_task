# celery_task

## celery 的定义

## 安装初始化

## celery的配置

### router


## 定义任务

## 高级设置

## AMPQ


## kombu

## 使用场景

## 启动命令

* 启动celery

```shell
celery -A tasks.main_tasks worker -Q push_queue -P gevent -c 2 --loglevel=info --logfile=./log.log
```
* tasks.main_tasks：指定任务文件
* -Q push_queue:指定队列任务，此消费者只消费此队列名为push_queue中的任务
* -P gevent -c 2：-P 指定并发的实现方式，常见的有prefork(default)/eventlet/gevent，-c 指定协程并发数
* -loglevel=info: 指定日志等级
* --logfile: 表示指定日志目录


* 启动周期/定时任务
启动beat之后还需要启动一个work进行消费，beat相当于是生产者，只会生成任务，而不会消费
```shell
celery -A tasks.main_tasks beat -l INFO --logfile=./beat.log
celery -A tasks.main_tasks worker -Q pull_queue -P gevent -c 2
```
>启动 beat 的时候，会发现启动的文件夹下会有一个名为 celerybeat-schedule.db 的文件，
这个是 beat 保存在本地的上一次任务运行的时间的数据，我们也可以指定该文件的输出地址：
celery -A tasks.main_tasks beat -l INFO -s ./celerybeat-schedule

