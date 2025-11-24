from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Category, SubCategory
from .serializers import (
    CategorySerializer,
    CategoryPageMetadataSerializer,
    CategorySlugSerializer,
    SubCategorySerializer
)


class CategoryViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Category.objects.all().order_by('order')
    lookup_field = 'slug'
    serializer_class = CategorySerializer

    @action(detail=True, methods=["get"], url_path="metadata")
    def metadata(self, request, slug=None):
        category = get_object_or_404(Category, slug=slug)
        serializer = CategoryPageMetadataSerializer(category, context={"request": request})
        return Response(serializer.data)

    @action(detail=False, methods=["get"], url_path="slugs")
    def slugs(self, request):
        category = Category.objects.all()
        serializer = CategorySlugSerializer(category, context={"request": request}, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["get"], url_path="page")
    def page(self, request, slug=None):
        category = get_object_or_404(Category, slug=slug)
        sub_categories = SubCategory.objects.filter(category=category)
        serializer = SubCategorySerializer(sub_categories, context={"request": request}, many=True)
        return Response(serializer.data)
