from django.shortcuts import render
from .models import HomeSlider  # import the new model
from apps.products.models import Product,Category


def index(request):
    
    sliders = HomeSlider.objects.filter(is_active=True).order_by('order')
    category_slug = request.GET.get('category')
# Sort products by newest first (for "New Arrivals")
    products = Product.objects.filter(is_available=True).order_by('-created_at')[:8]
    
    if category_slug:
        try:
            category = Category.objects.get(slug=category_slug)
            subcats = category.subcategories.all()
            products = products.filter(category__in=[category, *subcats])
        except Category.DoesNotExist:
            pass

    categories = Category.objects.filter(parent=None)  # top-level only
    return render(request, 'user_theme/store/index.html', {
        'sliders': sliders,
        'products': products,
        'categories': categories,
        'user': request.user  # now available in template

    })


# def admin_dashboard(request):
#     return render(request, 'admin/dashboard.html')
