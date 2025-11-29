from rest_framework import viewsets, mixins

from .models import Legal
from .serializers import LegalSerializer


class LegalViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Legal.objects.all()
    serializer_class = LegalSerializer
