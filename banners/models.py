from django.db import models
from django.core.validators import MinLengthValidator


class Banner(models.Model):
    title_en = models.CharField(
        verbose_name="English title",
        validators=[MinLengthValidator(2)],
        max_length=30,
        null=False,
        blank=False,
        help_text='min: 2, max: 30'
    )
    title_ro = models.CharField(
        verbose_name="Romanian title",
        validators=[MinLengthValidator(2)],
        max_length=30,
        null=False,
        blank=False,
        help_text='min: 2, max: 30'
    )
    sub_title_en = models.CharField(
        verbose_name="English sub title",
        validators=[MinLengthValidator(10)],
        max_length=50,
        null=False,
        blank=False,
        help_text='min: 10, max: 50'
    )
    sub_title_ro = models.CharField(
        verbose_name="Romanian sub title",
        validators=[MinLengthValidator(10)],
        max_length=50,
        null=False,
        blank=False,
        help_text='min: 10, max: 50'
    )
    image = models.ImageField(
        verbose_name="Image",
        upload_to="banners/",
        null=False,
        blank=False,
        help_text='accepted formats: jpg, webp'
    )
    text_color = models.CharField(
        verbose_name="Text color",
        validators=[MinLengthValidator(4)],
        max_length=7,
        null=False,
        blank=False,
        help_text='min: 4, max: 7. ex: #0000ff'
    )
    button_color = models.CharField(
        verbose_name="Button color",
        validators=[MinLengthValidator(4)],
        max_length=7,
        null=False,
        blank=False,
        help_text='min: 4, max: 7. ex: #0000ff'
    )
    button_text_color = models.CharField(
        verbose_name="Button text color",
        validators=[MinLengthValidator(4)],
        max_length=7,
        null=False,
        blank=False,
        help_text='min: 4, max: 7. ex: #0000ff'
    )
    order = models.PositiveIntegerField(verbose_name="Order number", null=False, blank=False)
    link = models.CharField(
        verbose_name="Link",
        max_length=255,
        null=False,
        blank=False,
        help_text='link to some page'
    )

    class Meta:
        verbose_name = "banner"
        verbose_name_plural = "banners"
        db_table = "banners"


class SubBanner(models.Model):
    title_en = models.CharField(
        verbose_name="English title",
        validators=[MinLengthValidator(2)],
        max_length=30,
        null=False,
        blank=False,
        help_text='min: 2, max: 30'
    )
    title_ro = models.CharField(
        verbose_name="Romanian title",
        validators=[MinLengthValidator(2)],
        max_length=30,
        null=False,
        blank=False,
        help_text='min: 2, max: 30'
    )
    sub_title_en = models.CharField(
        verbose_name="English sub title",
        validators=[MinLengthValidator(10)],
        max_length=50,
        null=False,
        blank=False,
        help_text='min: 10, max: 50'
    )
    sub_title_ro = models.CharField(
        verbose_name="Romanian sub title",
        validators=[MinLengthValidator(10)],
        max_length=50,
        null=False,
        blank=False,
        help_text='min: 10, max: 50'
    )
    image = models.ImageField(
        verbose_name="Image",
        upload_to="banners/",
        null=False,
        blank=False,
        help_text='accepted formats: jpg, webp'
    )
    text_color = models.CharField(
        verbose_name="Text color",
        validators=[MinLengthValidator(4)],
        max_length=7,
        null=False,
        blank=False,
        help_text='min: 4, max: 7. ex: #0000ff'
    )
    button_color = models.CharField(
        verbose_name="Button color",
        validators=[MinLengthValidator(4)],
        max_length=7,
        null=False,
        blank=False,
        help_text='min: 4, max: 7. ex: #0000ff'
    )
    button_text_color = models.CharField(
        verbose_name="Button text color",
        validators=[MinLengthValidator(4)],
        max_length=7,
        null=False,
        blank=False,
        help_text='min: 4, max: 7. ex: #0000ff'
    )
    order = models.PositiveIntegerField(verbose_name="Order number", null=False, blank=False)
    link = models.CharField(
        verbose_name="Link",
        max_length=255,
        null=False,
        blank=False,
        help_text='link to some page'
    )

    class Meta:
        verbose_name = "sub-banner"
        verbose_name_plural = "sub-banners"
        db_table = "sub_banners"
