import os
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver

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
