from django.shortcuts import render
from .models import HomeSlider  # import the new model
from apps.products.models import Product,Category
from django.db.models import Count
from apps.cart.models import CartItem


def index(request):
    
    sliders = HomeSlider.objects.filter(is_active=True).order_by('order')
    category_slug = request.GET.get('category')
    
    # New Arrivals - Latest products
    new_arrivals = Product.objects.filter(is_available=True).order_by('-created_at')[:8]
    
    # Best Sellers - Products with most cart additions (proxy for sales)
    best_sellers = Product.objects.filter(
        is_available=True
    ).annotate(
        cart_count=Count('cartitem')
    ).order_by('-cart_count')[:8]
    
    # If no best sellers based on cart, fallback to random products
    if not best_sellers:
        best_sellers = Product.objects.filter(is_available=True).order_by('?')[:8]
    
    # Categories - Top level only
    categories = Category.objects.filter(parent=None, is_active=True)[:6]
    
    return render(request, 'user_theme/store/index.html', {
        'sliders': sliders,
        'new_arrivals': new_arrivals,
        'best_sellers': best_sellers,
        'categories': categories,
        'user': request.user
    })
