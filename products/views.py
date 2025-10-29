from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Category, Product

def category_products(request, slug):
    category = get_object_or_404(Category, slug=slug)
    categories = Category.objects.filter(parent__isnull=True).prefetch_related('subcategories')
    subcategories = category.subcategories.all()
    products = Product.objects.filter(category__in=[category, *subcategories])
    return render(request, 'store/index.html', {
        'category': category,
        'categories': categories,
        'products': products,
        'selected_category': category,
    })

def filter_products_ajax(request, slug):
    category = get_object_or_404(Category, slug=slug)
    subcategories = Category.objects.filter(parent=category)
    products = Product.objects.filter(category__in=[category, *subcategories])
    data = [
        {
            "name": product.name,
            "price": product.price,
            "image": product.image.url if product.image else "",
            "category": product.category.category_name,
        }
        for product in products
    ]
    return JsonResponse({"products": data})

def cart_page(request):
    return render(request,'store/cart.html')

def cart_page1(request):
    return render(request,'store/cart2.html')

def checkout(request):
    return render(request,'store/checkout.html')