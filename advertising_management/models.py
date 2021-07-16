import datetime

from django.contrib.auth.models import User
from django.db import models


class Advertiser(models.Model):
    user = models.OneToOneField(to=User, related_name='advertisers', on_delete=models.CASCADE)
    name = models.CharField(max_length=30)


class Ad(models.Model):
    ad_owner = models.ForeignKey(Advertiser, on_delete=models.CASCADE, related_name='ads')
    title = models.CharField(max_length=30)
    link = models.URLField()
    img_url = models.URLField()
    is_approved = models.BooleanField(default=False)


class Impression(models.Model):
    class Meta:
        abstract = True

    involved_ad = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name="%(class)s_list")
    user_ip = models.GenericIPAddressField()
    impression_time = models.DateTimeField()


class Click(Impression):
    pass


class Seen(Impression):
    pass
