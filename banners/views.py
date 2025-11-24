from rest_framework import viewsets, mixins

from .models import Banner
from .serializers import BannerSerializer, SubBanner


class BannerViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer


class SubBannerViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = SubBanner.objects.all()
    serializer_class = BannerSerializer
