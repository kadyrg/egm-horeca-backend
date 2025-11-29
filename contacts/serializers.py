from rest_framework import serializers

from contacts.models import Contact


class ContactSerializer(serializers.ModelSerializer):
    label = serializers.SerializerMethodField()

    class Meta:
        model = Contact
        fields = ['id', 'label', 'link']

    def get_label(self, obj):
        request = self.context.get('request')
        lang = request.headers.get('Accept-Language', 'en').lower() if request else 'en'

        return obj.label_ro if 'ro' in lang else obj.label_en
