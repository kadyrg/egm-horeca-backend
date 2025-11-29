from rest_framework import serializers

from .models import Legal


class LegalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Legal
        fields = ['type', 'file']
