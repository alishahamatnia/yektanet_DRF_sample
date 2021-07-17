import datetime
from collections import defaultdict

from django.db.models import Count
from django.shortcuts import get_object_or_404
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

# Create your views here.
from .models import Ad, Seen, Click
from .serializers import AdSCreateSerializer, AdListSerializer, CLickSerializer, SeenSerializer


class AdViewSet(ModelViewSet):
    queryset = Ad.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = (SessionAuthentication, TokenAuthentication)

    def get_serializer_class(self):
        return AdSCreateSerializer if self.action == 'create' else AdListSerializer

    def get_queryset(self):
        if self.request.user.advertiser:
            result = self.request.user.advertiser.ads.all()
        result = Ad.objects.all()

        self.make_view(result)
        return result

    def make_view(self, ads):
        serializer1 = SeenSerializer(data=[dict() for _ in ads], many=True)
        serializer1.is_valid(raise_exception=True)

        serializer1.save(involved_ad=ads[0],
                         impression_time=datetime.datetime.now(),
                         user_ip=get_client_ip(self.request))

    def perform_create(self, serializer):
        serializer.save(ad_owner=self.request.user.advertiser)


class ClickCreateAPIView(CreateAPIView):
    serializer_class = CLickSerializer

    def perform_create(self, serializer):
        serializer.save(involved_ad=get_object_or_404(Ad, pk=self.kwargs['pk']),
                        impression_time=datetime.datetime.now(),
                        user_ip=get_client_ip(self.request))


class ReportApiView(APIView):

    def get(self, *args, **kwargs):
        clicks_report = Click.objects.values_list(
            'involved_ad',
            'impression_time',
            'user_ip',
        ).annotate(count=Count('id')).order_by('involved_ad', 'user_ip', 'impression_time')
        views_report = Seen.objects.values_list(
            'involved_ad',
            'impression_time',
            'user_ip',
        ).annotate(count=Count('id')).order_by('involved_ad', 'user_ip', 'impression_time')

        impression_report = defaultdict(lambda: defaultdict(lambda: {
            'clicked': 0,
            'viewed': 0
        }))

        impression_report_per_date = defaultdict(lambda: {
            'clicked': 0,
            'viewed': 0
        })

        total_clicked = 0
        total_viewed = 0
        for ad_id, impression_time, _, clicked in clicks_report:
            impression_report[ad_id][impression_time.strftime('%Y-%m-%dT%H')]['clicked'] += clicked
            impression_report_per_date[impression_time.strftime('%Y-%m-%dT%H')]['clicked'] += clicked
            total_clicked += clicked
        for ad_id, impression_time, _, viewed in views_report:
            impression_report[ad_id][impression_time.strftime('%Y-%m-%dT%H')]['viewed'] += viewed
            impression_report_per_date[impression_time.strftime('%Y-%m-%dT%H')]['viewed'] += viewed
            total_viewed += viewed

        click_per_view_report = dict(total=total_clicked / total_viewed if total_viewed else 1)
        for impression_date, impression_data in impression_report_per_date.items():
            click_per_view_report[impression_date] = impression_data['clicked'] / impression_data['viewed'] \
                if impression_data['viewed'] else 1

        clicked_viewed_average_time = 0
        for cli in clicks_report:
            # continue
            for i in range(len(views_report)):
                # continue
                vi = views_report[i]
                if vi[0] == cli[0] and vi[1] < cli[1] and vi[2] == cli[2]:
                    continue
                if cli[1] > views_report[i - 1 if i > 0 else 0][1]:
                    clicked_viewed_average_time += cli[1].timestamp() - views_report[i - 1 if i > 0 else 0][
                        1].timestamp()
                if vi[0] == cli[0] and vi[2] == cli[2]:
                    continue

        clicked_viewed_average_time /= len(clicks_report)

        return Response({
            'impression_report': impression_report,
            'click_per_view_report': click_per_view_report,
            'clicked_viewed_average_time': clicked_viewed_average_time

        })


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
