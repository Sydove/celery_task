from datetime import timedelta
from celery import Celery, platforms
from kombu import Exchange, Queue

# celery broker
CELERY_BROKER_URL = "redis://:123456@47.108.164.71:6379/1"

CELERY_QUEUES = (
    Queue(
        name="pull_queue",
        exchange=Exchange("data_tasks_exchange", "direct"),
        routing_key="pull_queue",
    ),
    Queue(
        name="push_queue",
        exchange=Exchange("data_tasks_exchange", "direct"),
        routing_key="push_queue",
    ),
)

"""
Exchange: 交换机
在 Celery 中，不同类型的交换机有以下几种：
Direct Exchange：生产者发布消息到直接交换机时，必须指定路由键。交换机仅将消息分配给与路由键完全匹配的队列。
Topic Exchange：生产者发布消息到主题交换机时，必须指定路由键。交换机根据路由键的词元匹配分配消息。
Fanout Exchange：生产者发布消息到扇出交换机时，不必指定路由键。扇出交换机将消息分配给所有与其绑定的队列。
对于不同的应用场景，使用不同类型的交换机可以提高系统的性能和灵活性。比如，如果您需要将生产者的消息发布到多个队列，则可以使用扇出交换机。如果您需要对生产者的消息进行路由，则可以使用直接交换机或主题交换机。
"""

CELERY_ROUTES = {
    "tasks.main_tasks.pull_task": {
        "queue": "pull_queue",
        "routing_key": "pull_queue",
    },
    "tasks.main_tasks.push_data_to_rpa": {
        "queue": "push_queue",
        "routing_key": "push_queue",
    },
    "tasks.main_tasks.update_task_status": {
        "queue": "push_queue",
        "routing_key": "push_queue",
    },
}

celery_app = Celery("test", broker=CELERY_BROKER_URL)
platforms.C_FORCE_ROOT = True
celery_app.conf.update(
    timezone="Asia/Shanghai",
    accept_content=["pickle", "json"],
    task_serializer="pickle",
    result_serializer="pickle",
    task_queues=CELERY_QUEUES,
    task_routes=CELERY_ROUTES,
    task_default_queue="default",
    broker_transport_options={
        "priority_steps": list(range(10)),
        "sep": ":",
        "queue_order_strategy": "priority",  # 优先级0-9， 0 优先级最高， 9 优先级最低
    },
    acks_late=True,
    worker_prefetch_multiplier=1,
    task_queue_max_priority=9,
    task_default_priority=9,
)
# 定时任务
celery_app.conf.beat_schedule = {
    'pull_task': {
        'task': 'tasks.main_tasks.pull_task',
        'schedule': timedelta(seconds=90),
        'args': ()
    },
}
