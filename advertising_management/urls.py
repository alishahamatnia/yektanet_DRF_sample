from django.contrib import admin
from django.urls import path
from advertising_management.views import *

urlpatterns = [
    path('ads/', AdViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('ads/<int:pk>/', AdViewSet.as_view({'get': 'retrieve', 'delete': 'destroy'})),
    path('ads/<int:pk>/click', ClickCreateAPIView.as_view()),


]
