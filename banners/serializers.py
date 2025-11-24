from rest_framework import serializers

from .models import Banner, SubBanner


class BannerSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    sub_title = serializers.SerializerMethodField()

    class Meta:
        model = Banner
        fields = ['id', 'title', 'sub_title', 'image', 'button_color', 'text_color', 'button_text_color', 'order']

    def get_title(self, obj):
        request = self.context.get('request')
        lang = request.headers.get('Accept-Language', 'en').lower() if request else 'en'

        return obj.title_ro if 'ro' in lang else obj.title_en

    def get_sub_title(self, obj):
        request = self.context.get('request')
        lang = request.headers.get('Accept-Language', 'en').lower() if request else 'en'

        return obj.sub_title_ro if 'ro' in lang else obj.sub_title_en


class SubBannerSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    sub_title = serializers.SerializerMethodField()

    class Meta:
        model = SubBanner
        fields = ['id', 'title', 'sub_title', 'image', 'button_color', 'text_color', 'button_text_color', 'order']

    def get_title(self, obj):
        request = self.context.get('request')
        lang = request.headers.get('Accept-Language', 'en').lower() if request else 'en'

        return obj.title_ro if 'ro' in lang else obj.title_en

    def get_sub_title(self, obj):
        request = self.context.get('request')
        lang = request.headers.get('Accept-Language', 'en').lower() if request else 'en'

        return obj.sub_title_ro if 'ro' in lang else obj.sub_title_en
