from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Product
from .serializers import (
    ProductPageMetadataSerializer,
    ProductDetailSerializer,
    ProductSlugSerializer,
    ProductListSerializer
)


class ProductViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Product.objects.filter(is_active=True)
    lookup_field = 'slug'
    serializer_class = ProductDetailSerializer

    @action(detail=True, methods=["get"], url_path="metadata")
    def metadata(self, request, slug=None):
        product = get_object_or_404(Product, slug=slug)
        serializer = ProductPageMetadataSerializer(product, context={"request": request})
        return Response(serializer.data)

    @action(detail=False, methods=["get"], url_path="slugs")
    def slugs(self, request):
        product = Product.objects.all()
        serializer = ProductSlugSerializer(product, context={"request": request}, many=True)
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ProductDetailSerializer
        if self.action == "list":
            return ProductListSerializer
