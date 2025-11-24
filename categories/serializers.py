from rest_framework import serializers

from products.serializers import ProductSerializer
from .models import Category, SubCategory


class CategorySerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'title', 'slug']

    def get_title(self, obj):
        request = self.context.get('request')
        lang = request.headers.get('Accept-Language', 'en').lower() if request else 'en'

        return obj.title_ro if 'ro' in lang else obj.title_en


class CategoryPageMetadataSerializer(serializers.ModelSerializer):
    meta_title = serializers.SerializerMethodField()
    meta_description = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['meta_title', 'meta_description']

    def get_meta_title(self, obj):
        request = self.context.get('request')
        lang = request.headers.get('Accept-Language', 'en').lower() if request else 'en'

        return obj.meta_title_ro if 'ro' in lang else obj.meta_title_en

    def get_meta_description(self, obj):
        request = self.context.get('request')
        lang = request.headers.get('Accept-Language', 'en').lower() if request else 'en'

        return obj.meta_title_ro if 'ro' in lang else obj.meta_title_en


class CategorySlugSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['slug']


class SubCategorySerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    products = ProductSerializer(many=True)

    class Meta:
        model = SubCategory
        fields = ['id', 'title', 'products']

    def get_title(self, obj):
        request = self.context.get('request')
        lang = request.headers.get('Accept-Language', 'en').lower() if request else 'en'

        return obj.title_ro if 'ro' in lang else obj.title_en
