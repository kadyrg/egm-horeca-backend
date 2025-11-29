from rest_framework import viewsets, mixins

from .models import Translation
from .serializers import TranslationSerializer


class TranslationViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Translation.objects.all()
    serializer_class = TranslationSerializer
