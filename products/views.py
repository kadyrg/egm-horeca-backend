from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Product
from .serializers import (
    ProductPageMetadataSerializer,
    ProductDetailSerializer,
    ProductSerializer
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

    @action(detail=True, methods=["get"], url_path="similar")
    def similar(self, request, slug=None):
        product = get_object_or_404(Product, slug=slug)
        similar_products = (
            Product.objects.filter(is_active=True, category=product.category)
            .exclude(id=product.pk)
            .order_by('?')[:6]
        )
        serializer = ProductSerializer(similar_products, many=True, context={"request": request})
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ProductDetailSerializer
        return ProductSerializer
