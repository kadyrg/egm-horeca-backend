import os
from django.db.models.signals import post_delete, pre_save, post_save
from django.dispatch import receiver
import httpx
from django.db import transaction

from backend import settings
from .models import Product, ProductImage


@receiver(post_delete, sender=Product)
def delete_image(sender, instance, **kwargs):
    if instance.main_image:
        if os.path.isfile(instance.main_image.path):
            os.remove(instance.main_image.path)


@receiver(pre_save, sender=Product)
def delete_old_image_on_update(sender, instance, **kwargs):
    if not instance.pk:
        return False
    try:
        old_image = Product.objects.get(pk=instance.pk).main_image
    except Product.DoesNotExist:
        return False

    new_image = instance.main_image
    if old_image and old_image != new_image:
        if os.path.isfile(old_image.path):
            os.remove(old_image.path)

@receiver(post_delete, sender=ProductImage)
def delete_file(sender, instance, **kwargs):
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)


@receiver(pre_save, sender=ProductImage)
def delete_old_file_on_update(sender, instance, **kwargs):
    if not instance.pk:
        return False
    try:
        old_file = ProductImage.objects.get(pk=instance.pk).image
    except ProductImage.DoesNotExist:
        return False

    new_file = instance.file
    if old_file and old_file != new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)


# @receiver(pre_save, sender=Product)
# def send_slug_to_frontend(sender, instance, **kwargs):
#     def _revalidate():
#         payload = {"tags": ['products'], "paths": [f"/en/{instance.slug}", f"/ro/{instance.slug}"]}
#         headers = {"Content-Type": "application/json"}
#         try:
#             with httpx.Client(timeout=5, verify=settings.ENV == "production") as client:
#                 client.request("POST", settings.REVALIDATE_API, json=payload, headers=headers)
#         except Exception as e:
#             print(f"Failed to send slug to frontend: {e}")
#
#     transaction.on_commit(_revalidate)
#

# @receiver(post_save, sender=Product)
# def send_product_slug_to_frontend(sender, instance, created, **kwargs):
#     def _send():
#         frontend_endpoint = f"{settings.FRONTEND_URL}/api/revalidate/products"
#         payload = {
#             "categorySlug": instance.category.category.slug,
#             "slug": instance.slug,
#         }
#
#         if not created:
#             old_category_slug = getattr(instance, "_old_category_slug", None)
#             if old_category_slug and old_category_slug != instance.category.category.slug:
#                 payload["oldCategorySlug"] = old_category_slug
#
#         method = "POST" if created else "PUT"
#         headers = {"Content-Type": "application/json"}
#
#         try:
#             with httpx.Client(timeout=5, verify=(settings.ENV == "production")) as client:
#                 client.request(method, frontend_endpoint, json=payload, headers=headers)
#         except Exception as e:
#             print(f"Failed to send product revalidation info: {e}")
#
#     transaction.on_commit(_send)
