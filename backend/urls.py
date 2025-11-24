from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers

from payments.views import create_checkout_session, stripe_webhook
from categories.views import CategoryViewSet
from products.views import ProductViewSet
from banners.views import BannerViewSet, SubBannerViewSet


router = routers.DefaultRouter()

router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'products', ProductViewSet, basename='products')
router.register(r'banners', BannerViewSet, basename='banners')
router.register(r'sub_banners', SubBannerViewSet, basename='sub_banners')

urlpatterns = [
    path('api/', include(router.urls)),
    path('', admin.site.urls),
    path("api/create-checkout-sessio/", create_checkout_session),
    path("api/payments/webhook/", stripe_webhook),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
