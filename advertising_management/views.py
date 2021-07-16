import datetime
import time

from django.shortcuts import get_object_or_404
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.generics import CreateAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

# Create your views here.
from .models import Ad
from .serializers import AdSCreateSerializer, AdListSerializer, CLickSerializer, SeenSerializer


class AdViewSet(ModelViewSet):
    queryset = Ad.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = (SessionAuthentication, TokenAuthentication)

    def get_serializer_class(self):
        return AdSCreateSerializer if self.action == 'create' else AdListSerializer

    def get_queryset(self):
        if self.request.user.advertiser:
            return self.request.user.advertiser.ads.all()
        return Ad.objects.all()

    def perform_create(self, serializer):
        serializer.save(ad_owner=self.request.user.advertiser)


class ClickCreateAPIView(CreateAPIView):
    serializer_class = CLickSerializer

    def get_client_ip(self):
        request = self.request
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def perform_create(self, serializer):
        serializer.save(involved_ad=get_object_or_404(Ad, pk=self.kwargs['pk']),
                        impression_time=datetime.datetime.now(),
                        user_ip=self.get_client_ip())
