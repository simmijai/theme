from products.models import Product
from django.shortcuts import render, redirect, get_object_or_404


def product_list(request):
    products = Product.objects.select_related('category').all()
    return render(request, 'admin/product.html', {'products': products})




