from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

# Create your views here.
from .models import Ad
from .serializers import AdSCreateSerializer, AdListSerializer


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


