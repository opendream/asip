from celery.task import task
from common.models import StatisitcAccess


@task()
def task_create_statistic_access(content_type, object_id, ip_address):
    StatisitcAccess.objects.create(content_type=content_type, object_id=object_id, ip_address=ip_address)
