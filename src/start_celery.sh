mkdir celery_logs
celery -A tasks.main_tasks beat
celery -A tasks.main_tasks worker -Q pull_queue --loglevel=info --logfile="./celery_logs/pull_celery.log" # 拉取任务work
celery -A tasks.main_tasks worker -Q push_queue --loglevel=info --logfile="./celery_log/push_celery.log" # 推送任务work
