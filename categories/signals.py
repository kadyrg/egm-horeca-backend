from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Category
import httpx
from django.db import transaction

from backend import settings


@receiver(post_save, sender=Category)
def send_slug_to_frontend(sender, instance, created, **kwargs):
    def _revalidate():
        payload = {"tags": ['categories'], "paths": [f"/en/{instance.slug}", f"/ro/{instance.slug}"]}
        headers = {"Content-Type": "application/json"}
        try:
            with httpx.Client(timeout=5, verify=settings.ENV == "production") as client:
                client.request("POST", settings.REVALIDATE_API, json=payload, headers=headers)
        except Exception as e:
            print(f"Failed to send slug to frontend: {e}")
    transaction.on_commit(_revalidate)


@receiver(post_delete, sender=Category)
def delete_category_revalidate(sender, instance, **kwargs):
    def _revalidate():
        payload = {"tags": ['categories'], "paths": [f"/en/{instance.slug}", f"/ro/{instance.slug}"]}
        headers = {"Content-Type": "application/json"}
        try:
            with httpx.Client(timeout=5, verify=settings.ENV == "production") as client:
                client.request("POST", settings.REVALIDATE_API, json=payload, headers=headers)
        except Exception as e:
            print(f"Failed to revalidate frontend on delete: {e}")
    transaction.on_commit(_revalidate)
