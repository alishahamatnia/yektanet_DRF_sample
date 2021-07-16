from rest_framework import serializers
from models import Ad, Advertiser, Click, Seen


class AdvertiserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertiser
        fields = ['name']


class AdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = ['ad_owner', 'title', 'img_url', 'link', 'is_approved']


class CLickSerializer(serializers.ModelSerializer):
    class Meta:
        model = Click
        fields = ['involved_ad', 'user_ip', 'impression_time']


class SeenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seen
        fields = ['involved_ad', 'user_ip', 'impression_time']
