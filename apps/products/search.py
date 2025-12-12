from django.db.models import Q
from .models import Product

def search_products(query):
    if not query:
        return Product.objects.none()
    
    return Product.objects.filter(
        Q(name__icontains=query) |
        Q(description__icontains=query) |
        Q(category__category_name__icontains=query)
    ).distinct()