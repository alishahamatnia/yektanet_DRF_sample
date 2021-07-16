from rest_framework import serializers
from .models import Ad, Advertiser, Click, Seen


class AdvertiserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertiser
        fields = ['name']


class AdSCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = ['id', 'title', 'img_url', 'link', 'is_approved']


class AdListSerializer(AdSCreateSerializer):
    class Meta(AdSCreateSerializer.Meta):
        fields = AdSCreateSerializer.Meta.fields + ['ad_owner']


class AdvertiserAdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertiser
        fields = ['name', 'ads']


class CLickSerializer(serializers.ModelSerializer):
    class Meta:
        model = Click
        fields = ['involved_ad', 'user_ip', 'impression_time']


class SeenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seen
        fields = ['involved_ad', 'user_ip', 'impression_time']
