from rest_framework import viewsets, mixins

from contacts.models import Contact
from contacts.serializers import ContactSerializer


class ContactViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
