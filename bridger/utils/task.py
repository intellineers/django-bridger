from celery import shared_task


@shared_task
def save_as_task(obj):
    obj.save()