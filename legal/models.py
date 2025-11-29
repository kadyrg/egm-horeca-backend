from django.db import models


class LegalType(models.TextChoices):
    PRIVACY_POLICY_EN = 'PRIVACY_POLICY_EN'
    PRIVACY_POLICY_RO = 'PRIVACY_POLICY_RO'
    TERMS_AND_CONDITIONS_EN = 'TERMS_AND_CONDITIONS_EN'
    TERMS_AND_CONDITIONS_RO = 'TERMS_AND_CONDITIONS_RO'

class Legal(models.Model):
    type = models.CharField(choices=LegalType.choices, max_length=50, null=False, blank=False, unique=True)
    file = models.FileField(upload_to='legal', null=False, blank=False)

    class Meta:
        verbose_name = "legal"
        verbose_name_plural = "legals"
        db_table = "legals"
