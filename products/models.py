from django.db import models
from django.core.validators import MinLengthValidator
from django.utils.text import slugify

from categories.models import SubCategory


class Product(models.Model):
    title_en = models.CharField(
        verbose_name="English title",
        validators=[MinLengthValidator(5)],
        max_length=150,
        null=False,
        blank=False,
        help_text='min: 5, max: 150'
    )
    title_ro = models.CharField(
        verbose_name="Romanian title",
        validators=[MinLengthValidator(5)],
        max_length=150,
        null=False,
        blank=False,
        help_text='min: 5, max: 150'
    )
    description_en = models.TextField(
        verbose_name="English description",
        validators=[MinLengthValidator(10)],
        max_length=2000,
        null=True,
        blank=True,
        help_text='min: 10, max: 2000'
    )
    description_ro = models.TextField(
        verbose_name="Romanian description",
        validators=[MinLengthValidator(10)],
        max_length=2000,
        null=True,
        blank=True,
        help_text='min: 10, max: 2000'
    )
    brand_title = models.CharField(
        verbose_name="Brand title",
        validators=[MinLengthValidator(1)],
        max_length=150,
        null=True,
        blank=True,
        help_text='min: 1, max: 150'
    )
    slug = models.SlugField(
        verbose_name="Slug",
        validators=[MinLengthValidator(5)],
        max_length=150,
        null=False,
        blank=False,
        editable=False,
        help_text='min: 5, max: 150'
    )
    old_price = models.DecimalField(
        verbose_name="Old price",
        decimal_places=2,
        max_digits=10,
        null=True,
        blank=True,
        help_text="max_digits: 10, decimal_places: 2. Currency: Romanian Lei"
    )
    price = models.DecimalField(
        verbose_name="Price",
        decimal_places=2,
        max_digits=10,
        null=True,
        blank=True,
        help_text="max_digits: 10, decimal_places: 2. Currency: Romanian Lei"
    )
    stock = models.PositiveIntegerField(
        verbose_name="Stock",
        null=False,
        blank=False,
        help_text="Stock count"
    )
    main_image = models.ImageField(
        verbose_name="Main image",
        upload_to="products/",
        null=False,
        blank=False,
        help_text='aspect: 3/4'
    )
    is_active = models.BooleanField(verbose_name="Status", default=True, null=False, blank=False)
    category = models.ForeignKey(
        SubCategory,
        verbose_name="Category",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name="products"
    )
    order = models.PositiveIntegerField(
        verbose_name="Order number",
        null=False,
        blank=False,
        help_text='Order number'
    )
    created_at = models.DateTimeField(
        verbose_name="Created at",
        auto_now_add=True,
        null=False,
        blank=False,
        editable=False,
        help_text='Created datetime'
    )
    updated_at = models.DateTimeField(
        verbose_name="Updated at",
        auto_now=True,
        null=False,
        blank=False,
        editable=False,
        help_text='Updated datetime'
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title_en)
            slug = base_slug
            counter = 1
            while Product.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title_en

    class Meta:
        verbose_name = "product"
        verbose_name_plural = "products"
        db_table = "products"


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images",
        null=False,
        blank=False
    )
    image = models.ImageField(
        verbose_name="Image",
        upload_to="products/",
        null=False,
        blank=False,
        help_text='accepted formats: png'
    )
    order = models.PositiveIntegerField(verbose_name="Order number", null=False, blank=False)

    class Meta:
        verbose_name = "product-image"
        verbose_name_plural = "product-images"
        db_table = "product_images"


class ProductAttribute(models.Model):
    product = models.OneToOneField(
        Product,
        verbose_name="Product",
        on_delete=models.CASCADE,
        related_name="attribute",
        null=False,
        blank=False,
        help_text='product attribute'
    )
    title_en = models.CharField(
        verbose_name="English title",
        validators=[MinLengthValidator(1)],
        max_length=30,
        null=False,
        blank=False,
        help_text='min: 1, max: 30'
    )
    title_ro = models.CharField(
        verbose_name="Romanian title",
        validators=[MinLengthValidator(1)],
        max_length=30,
        null=False,
        blank=False,
        help_text='min: 1, max: 30'
    )

    def __str__(self):
        return self.title_en

    class Meta:
        verbose_name = "product-attribute"
        verbose_name_plural = "product-attributes"
        db_table = "product_attributes"


class ProductAttributeItem(models.Model):
    attribute = models.ForeignKey(
        ProductAttribute,
        verbose_name="Attribute Item",
        on_delete=models.CASCADE,
        related_name="items",
        null=False,
        blank=False,
        help_text='product attribute item'
    )
    title_en = models.CharField(
        verbose_name="English title",
        validators=[MinLengthValidator(1)],
        max_length=30,
        null=False,
        blank=False,
        help_text='min: 1, max: 30'
    )
    title_ro = models.CharField(
        verbose_name="Romanian title",
        validators=[MinLengthValidator(1)],
        max_length=30,
        null=False,
        blank=False,
        help_text='min: 1, max: 30'
    )
    old_price = models.DecimalField(
        verbose_name="Old price",
        decimal_places=2,
        max_digits=10,
        null=True,
        blank=True,
        help_text="max_digits: 10, decimal_places: 2. Currency: Romanian Lei"
    )
    price = models.DecimalField(
        verbose_name="Price",
        decimal_places=2,
        max_digits=10,
        null=True,
        blank=True,
        help_text="max_digits: 10, decimal_places: 2. Currency: Romanian Lei"
    )
    stock = models.PositiveIntegerField(
        verbose_name="Stock",
        null=False,
        blank=False,
        help_text="Stock count"
    )

    def __str__(self):
        return self.title_en

    class Meta:
        verbose_name = "product-attribute-item"
        verbose_name_plural = "product-attribute-items"
        db_table = "product_attribute_items"
