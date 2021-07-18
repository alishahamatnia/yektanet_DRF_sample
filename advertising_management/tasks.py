import datetime

from celery import task
from celery import shared_task
# We can have either registered task
from .models import *


@task(name='last_hour_report')
def send_import_summary():
    view_count = len(Ad.objects.filter('impression_time__date' == datetime.datetime.now().date,
                                       'impression_time__hour' == datetime.datetime.now().hour))
    click_count = len(Click.objects.filter('impression_time__date' == datetime.datetime.now().date,
                                           'impression_time__hour' == datetime.datetime.now().hour))

    Report(period='hourly', click_count=click_count, view_count=view_count, report_time=datetime.datetime.now()).save()
