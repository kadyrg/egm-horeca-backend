from django.db import models


class Translation(models.Model):
    key = models.CharField(verbose_name="Key", null=False, blank=False, unique=True, help_text="Key of a value")
    value_en = models.CharField(verbose_name="English value", null=False, blank=False, help_text="English value")
    value_ro = models.CharField(verbose_name="Romanian value", null=False, blank=False, help_text="Romanian value")
