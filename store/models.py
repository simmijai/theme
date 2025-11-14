from django.db import models

class HomeSlider(models.Model):
    title = models.CharField(max_length=150, default="Shop Our New Collection")
    subtitle = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to='sliders/')
    button_text = models.CharField(max_length=50, default="Shop Now")
    button_link = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0, help_text="Lower number = higher priority")

    class Meta:
        ordering = ['order']
        verbose_name = "Home Slider"
        verbose_name_plural = "Home Sliders"

    def __str__(self):
        return self.title


# products/models.py (or a new reviews.py if you prefer)

from django.db import models
from django.conf import settings
from products.models import Product
from orders.models import Order

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField(default=5)  # 1-5 stars
    comment = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='review_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('product', 'user')  # One review per product per user
        ordering = ['-created_at']  # newest first

    def __str__(self):
        return f"{self.user.email} - {self.product.name} ({self.rating}★)"
