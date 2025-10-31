from django.db import models
from django.utils.text import slugify

class Category(models.Model):
    category_name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField(blank=True, null=True)
    cat_image = models.ImageField(upload_to='category_images/', blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategories')

    class Meta:
        verbose_name_plural = 'Categories'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.category_name)
        super().save(*args, **kwargs)

    def __str__(self):
        full_name = self.category_name
        if self.parent:
            full_name = f"{self.parent.category_name} > {self.category_name}"
        return full_name

class Product(models.Model):
    category        = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name            = models.CharField(max_length=200)
    slug            = models.SlugField(unique=True, blank=True)
    description     = models.TextField()
    price           = models.DecimalField(max_digits=10, decimal_places=2)
    image           = models.ImageField(upload_to='products/')
    stock           = models.PositiveIntegerField()
    is_available    = models.BooleanField(default=True)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/')
    is_default = models.BooleanField(default=False)  # first image to show

    def __str__(self):
        return f"{self.product.name} Image"

class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    color = models.CharField(max_length=50, blank=True, null=True)
    size = models.CharField(max_length=50, blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # optional variant price

    def __str__(self):
        return f"{self.product.name} - {self.color or ''} {self.size or ''}"

class ProductAttribute(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='attributes')
    key = models.CharField(max_length=100)    # e.g., "Material", "Seater"
    value = models.CharField(max_length=255)  # e.g., "Cotton", "3-Seater"

    def __str__(self):
        return f"{self.product.name} → {self.key}: {self.value}"

