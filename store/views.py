from django.shortcuts import render
from products.models import Product,Category


def index(request):
    category_slug = request.GET.get('category')
    products = Product.objects.all()

    if category_slug:
        try:
            category = Category.objects.get(slug=category_slug)
            subcats = category.subcategories.all()
            products = products.filter(category__in=[category, *subcats])
        except Category.DoesNotExist:
            pass

    categories = Category.objects.filter(parent=None)  # top-level only
    return render(request, 'store/index.html', {
        'products': products,
        'categories': categories,
        'user': request.user  # now available in template

    })


# def admin_dashboard(request):
#     return render(request, 'admin/dashboard.html')