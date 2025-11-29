from django.db import models
from django.core.validators import MinLengthValidator


class Contact(models.Model):
    label_en = models.CharField(
        verbose_name="English label",
        validators=[MinLengthValidator(1)],
        max_length=30,
        null=False,
        blank=False,
        help_text="min: 1, max: 30"
    )
    label_ro = models.CharField(
        verbose_name="Romanian label",
        validators=[MinLengthValidator(1)],
        max_length=30,
        null=False,
        blank=False,
        help_text="min: 1, max: 30"
    )
    link = models.CharField(
        verbose_name="Link",
        validators=[MinLengthValidator(1)],
        max_length=255,
        null=False,
        blank=False,
        help_text="min: 1, max: 255"
    )

    class Meta:
        verbose_name = "contact"
        verbose_name_plural = "contacts"
        db_table = "contacts"
