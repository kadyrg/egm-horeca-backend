from rest_framework import serializers

from .models import Product, ProductImage, ProductAttribute, ProductAttributeItem


class ProductSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', "title", 'main_image', 'slug', "price", 'old_price']

    def get_title(self, obj):
        request = self.context.get('request')
        lang = request.headers.get('Accept-Language', 'en').lower() if request else 'en'

        return obj.title_ro if 'ro' in lang else obj.title_en


class ProductPageMetadataSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ["title", 'description']

    def get_title(self, obj):
        request = self.context.get('request')
        lang = request.headers.get('Accept-Language', 'en').lower() if request else 'en'

        return obj.title_ro if 'ro' in lang else obj.title_en

    def get_description(self, obj):
        request = self.context.get('request')
        lang = request.headers.get('Accept-Language', 'en').lower() if request else 'en'

        return obj.description_ro if 'ro' in lang else obj.description_en


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image']


class ProductAttributeItemSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()

    class Meta:
        model = ProductAttributeItem
        fields = ['id', 'title', 'price', 'old_price', 'stock']

    def get_title(self, obj):
        request = self.context.get('request')
        lang = request.headers.get('Accept-Language', 'en').lower() if request else 'en'

        return obj.title_ro if 'ro' in lang else obj.title_en


class ProductAttributeSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    items = ProductAttributeItemSerializer(many=True)

    class Meta:
        model = ProductAttribute
        fields = ['title', 'items']

    def get_title(self, obj):
        request = self.context.get('request')
        lang = request.headers.get('Accept-Language', 'en').lower() if request else 'en'

        return obj.title_ro if 'ro' in lang else obj.title_en


class ProductDetailSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    images = ProductImageSerializer(many=True)
    attribute = ProductAttributeSerializer()

    class Meta:
        model = Product
        fields = [
            "id",
            "title",
            "description",
            "brand_title",
            'main_image',
            "images",
            "price",
            'old_price',
            'stock',
            'attribute'
        ]

    def get_title(self, obj):
        request = self.context.get('request')
        lang = request.headers.get('Accept-Language', 'en').lower() if request else 'en'

        return obj.title_ro if 'ro' in lang else obj.title_en

    def get_description(self, obj):
        request = self.context.get('request')
        lang = request.headers.get('Accept-Language', 'en').lower() if request else 'en'

        return obj.description_ro if 'ro' in lang else obj.description_en


class ProductListSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'title', 'main_image', 'slug', 'price', 'old_price', 'brand_title']

    def get_title(self, obj):
        request = self.context.get('request')
        lang = request.headers.get('Accept-Language', 'en').lower() if request else 'en'

        return obj.title_ro if 'ro' in lang else obj.title_en


class ProductSlugSerializer(serializers.ModelSerializer):
    category_slug = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['slug', 'category_slug']

    def get_category_slug(self, obj):
        return obj.category.category.slug
