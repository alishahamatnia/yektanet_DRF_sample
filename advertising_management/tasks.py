import datetime

from celery import task
from celery import shared_task
# We can have either registered task
from .models import *


@task(name='last_hour_report')
def hourly_report():
    view_count = len(Ad.objects.filter('impression_time__date' == datetime.datetime.now().date,
                                       'impression_time__hour' == datetime.datetime.now().hour))
    click_count = len(Click.objects.filter('impression_time__date' == datetime.datetime.now().date,
                                           'impression_time__hour' == datetime.datetime.now().hour))

    Report(period='hourly', click_count=click_count, view_count=view_count, report_time=datetime.datetime.now()).save()


@task(name='last_day_report')
def daily_report():
    reports = Report.objects.filter('period' == 'hourly',
                                    'report_time__date' == datetime.datetime.now().date)
    view_count = click_count = 0
    for r in reports:
        view_count += int(r.view_count)
        click_count += int(r.click_count)

    Report(period='daily', report_time=datetime.datetime.now(), click_count=click_count, view_count=view_count).save()
