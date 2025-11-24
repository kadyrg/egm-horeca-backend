from django.db import models
from django.core.validators import MinLengthValidator


class EntityTypeEnum(models.TextChoices):
    INDIVIDUAL = "INDIVIDUAL"
    COMPANY = "COMPANY"


class OrderStatusEnum(models.TextChoices):
    PENDING = "PENDING"
    ACTIVE = "ACTIVE"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    DECLINED = "DECLINED"


class Order(models.Model):
    entity_type = models.CharField(
        verbose_name="Entity type",
        choices=EntityTypeEnum.choices,
        null=False,
        blank=False,
        help_text='choices: INDIVIDUAL, COMPANY'
    )
    email = models.EmailField(
        verbose_name="Email",
        null=False,
        blank=False,
        help_text='Email address'
    )
    first_name = models.CharField(
        verbose_name="First name",
        validators=[MinLengthValidator(2)],
        max_length=25,
        null=False,
        blank=False,
        help_text='min: 2, max: 25'
    )
    last_name = models.CharField(
        verbose_name="Last name",
        validators=[MinLengthValidator(2)],
        max_length=25,
        null=False,
        blank=False,
        help_text='min: 2, max: 25'
    )
    phone_number = models.CharField(
        verbose_name="Phone number",
        max_length=50,
        null=False,
        blank=False,
    )
    status = models.CharField(
        verbose_name="Status",
        choices=OrderStatusEnum.choices,
        default=OrderStatusEnum.PENDING,
        null=False,
        blank=False,
    )
    country = models.CharField(
        verbose_name="Country",
        max_length=250,
        null=False,
        blank=False,
    )
    city = models.CharField(
        verbose_name="City",
        max_length=250,
        null=False,
        blank=False,
    )
    postal_code = models.CharField(
        verbose_name="Postal code",
        max_length=50,
        null=False,
        blank=False,
    )
    street = models.CharField(
        verbose_name="Street",
        max_length=250,
        null=False,
        blank=False,
    )
    house_number = models.CharField(
        verbose_name="House number",
        max_length=50,
        null=False,
        blank=False,
    )
    created_at = models.DateTimeField(
        verbose_name="Created at",
        auto_now_add=True,
        null=False,
        blank=False,
    )

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "order"
        verbose_name_plural = "orders"
        db_table = "orders"
