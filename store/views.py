from django.shortcuts import render
from products.models import Product

def index(request):
    products = Product.objects.all()  # get all products
    return render(request, 'store/index.html', {'products': products})
