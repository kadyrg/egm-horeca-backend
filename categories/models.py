from django.db import models
from django.core.validators import MinLengthValidator
from django.utils.text import slugify


class Category(models.Model):
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
    meta_title_en = models.CharField(
        verbose_name="English meta title",
        validators=[MinLengthValidator(10)],
        max_length=50,
        null=False,
        blank=False,
        help_text='min: 10, max: 50'
    )
    meta_title_ro = models.CharField(
        verbose_name="Romanian meta title",
        validators=[MinLengthValidator(10)],
        max_length=50,
        null=False,
        blank=False,
        help_text='min: 10, max: 50'
    )
    meta_description_en = models.TextField(
        verbose_name="English meta description",
        validators=[MinLengthValidator(25)],
        max_length=150,
        null=False,
        blank=False,
        help_text='min: 25, max: 150'
    )
    meta_description_ro = models.TextField(
        verbose_name="Romanian meta description",
        validators=[MinLengthValidator(25)],
        max_length=150,
        null=False,
        blank=False,
        help_text='min: 25, max: 150'
    )
    order = models.PositiveIntegerField(verbose_name="Order number", null=False, blank=False)
    slug = models.SlugField(
        verbose_name="Slug",
        validators=[MinLengthValidator(2)],
        max_length=25,
        unique=True,
        null=False,
        blank=False,
        editable=False,
        help_text='min: 2, max: 25'
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title_en)
            slug = base_slug
            counter = 1
            while Category.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title_en

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"
        db_table = "categories"


class SubCategory(models.Model):
    category = models.ForeignKey(
        Category,
        verbose_name="Parent category",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name="sub_categories"
    )
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
    order = models.PositiveIntegerField(verbose_name="Order number", null=False, blank=False)

    def __str__(self):
        return self.title_en

    class Meta:
        verbose_name = "sub-category"
        verbose_name_plural = "sub-categories"
        db_table = "sub_categories"
