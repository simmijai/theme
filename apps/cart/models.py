from django.db import models
from django.conf import settings
from apps.products.models import Product

class CartItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')  # prevents duplicate cart items

    def __str__(self):
        return f"{self.user.username} - {self.product.name} ({self.quantity})"

    def total_price(self):
        """Returns total price for this item"""
        if self.product.price:
            return self.quantity * self.product.price
        return 0
