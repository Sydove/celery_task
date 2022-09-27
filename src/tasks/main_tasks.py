from confs.celery_conf import celery_app


@celery_app.task
def pull_task():
    """
    轮询SQLServer，获取任务
    """
    print("执行任务拉取作业")


@celery_app.task
def update_task_status(result):
    """
    更新推送结果给SQLServer
    """
    print(result)
    print("更新推送结果给SQLServer")


@celery_app.task
def push_data_to_rpa():
    """
    推送任务给RPA中台
    """
    print("推送数据给中台")
    update_task_status.apply_async(args=("1",))
