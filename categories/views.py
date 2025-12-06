from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Count, Q

from .models import Category, SubCategory
from .serializers import (
    CategorySerializer,
    CategoryPageMetadataSerializer,
    SubCategorySerializer
)


class CategoryViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Category.objects.all().order_by('order')
    lookup_field = 'slug'
    serializer_class = CategorySerializer

    @action(detail=True, methods=["get"], url_path="metadata")
    def metadata(self, request, slug=None):
        category = get_object_or_404(Category, slug=slug)
        serializer = CategoryPageMetadataSerializer(category, context={"request": request})
        return Response(serializer.data)

    @action(detail=True, methods=["get"], url_path="sub-categories")
    def sub_categories(self, request, slug=None):
        category = get_object_or_404(Category, slug=slug)
        sub_categories = (
            SubCategory.objects.filter(category=category)
            .annotate(
                product_count=Count("products", filter=Q(products__is_active=True))
            )
            .filter(product_count__gt=0)
        )
        serializer = SubCategorySerializer(sub_categories, context={"request": request}, many=True)
        return Response(serializer.data)
