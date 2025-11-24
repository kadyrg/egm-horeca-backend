import os
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver

from .models import Banner, SubBanner

#
# @receiver(post_delete, sender=Banner)
# def delete_image(sender, instance, **kwargs):
#     if instance.image:
#         if os.path.isfile(instance.image.path):
#             os.remove(instance.image.path)
#
#
# @receiver(pre_save, sender=Banner)
# def delete_old_image_on_update(sender, instance, **kwargs):
#     if not instance.pk:
#         return False
#     try:
#         old_image = Banner.objects.get(pk=instance.pk).image
#     except Banner.DoesNotExist:
#         return False
#
#     new_image = instance.image
#     if old_image and old_image != new_image:
#         if os.path.isfile(old_image.path):
#             os.remove(old_image.path)
#
#
# @receiver(post_delete, sender=SubBanner)
# def delete_image(sender, instance, **kwargs):
#     if instance.image:
#         if os.path.isfile(instance.image.path):
#             os.remove(instance.image.path)
#
#
# @receiver(pre_save, sender=SubBanner)
# def delete_old_image_on_update(sender, instance, **kwargs):
#     if not instance.pk:
#         return False
#     try:
#         old_image = SubBanner.objects.get(pk=instance.pk).image
#     except SubBanner.DoesNotExist:
#         return False
#
#     new_image = instance.image
#     if old_image and old_image != new_image:
#         if os.path.isfile(old_image.path):
#             os.remove(old_image.path)
