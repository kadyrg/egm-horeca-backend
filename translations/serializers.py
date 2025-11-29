from rest_framework import serializers

from .models import Translation


class TranslationSerializer(serializers.ModelSerializer):
    value = serializers.SerializerMethodField()

    class Meta:
        model = Translation
        fields = ['key', 'value']

    def get_value(self, obj):
        request = self.context.get('request')
        lang = request.headers.get('Accept-Language', 'en').lower() if request else 'en'

        return obj.value_ro if 'ro' in lang else obj.value_en
