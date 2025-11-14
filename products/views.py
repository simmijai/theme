from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Category, Product

# def category_products(request, slug):
#     category = get_object_or_404(Category, slug=slug)
#     categories = Category.objects.filter(parent__isnull=True).prefetch_related('subcategories')
#     subcategories = category.subcategories.all()
#     products = Product.objects.filter(category__in=[category, *subcategories])
#     return render(request, 'store/index.html', {
#         'category': category,
#         'categories': categories,
#         'products': products,
#         'selected_category': category,
#     })

def category_products(request, slug):
    # Try main category first
    category = Category.objects.filter(slug=slug, parent__isnull=True).first()
    subcategory = Category.objects.filter(slug=slug, parent__isnull=False).first()

    if subcategory:
        # If slug is a subcategory, get its parent for sidebar
        products = Product.objects.filter(category=subcategory)
        category = subcategory.parent
    else:
        # If main category, include subcategories
        subcategories = category.subcategories.all()
        products = Product.objects.filter(category__in=[category, *subcategories])

    categories = Category.objects.filter(parent__isnull=True).prefetch_related('subcategories')

    return render(request, 'store/product_category_page.html', {
        'category': category,
        'categories': categories,
        'products': products,
        'selected_category': slug,  # use slug for active highlighting
    })

from django.shortcuts import render, get_object_or_404
from .models import Category, Product

def subcategory_products(request, slug):
    subcategory = get_object_or_404(Category, slug=slug, parent__isnull=False)
    
    # Get all products in this subcategory
    products = Product.objects.filter(category=subcategory)
    
    # Get the 'sort' parameter from GET request
    sort = request.GET.get('sort', '')
    
    # Apply sorting
    if sort == 'title-ascending':
        products = products.order_by('name')
    elif sort == 'title-descending':
        products = products.order_by('-name')
    elif sort == 'price-ascending':
        products = products.order_by('price')
    elif sort == 'price-descending':
        products = products.order_by('-price')
    elif sort == 'newest':
        products = products.order_by('-created_at')
    elif sort == 'oldest':
        products = products.order_by('created_at')
    elif sort == 'best-selling':
        # products = products.annotate(sales_count=Sum('order_items__quantity')).order_by('-sales_count')
        pass  # replace with real logic if you have sales data

    context = {
        'subcategory': subcategory,
        'products': products,
        'sort': sort,
        'product_count': products.count(),
        'top_categories': Category.objects.filter(parent=None),  # for navbar/sidebar
    }
    
    return render(request, 'store/product_subcategory.html', context)


# def product_detail(request, slug):
#     product = get_object_or_404(Product, slug=slug)
#     return render(request, 'store/product_detail.html', {'product': product})

from orders.models import OrderItem

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    user = request.user
    show_review_button = False
    existing_review = None

    if user.is_authenticated:
        # Check if user has delivered orders with this product
        delivered_orders = OrderItem.objects.filter(
            order__user=user,
            order__status='Delivered',
            product=product
        )
        if delivered_orders.exists():
            show_review_button = True

        # Check if user has already submitted a review
        existing_review = product.reviews.filter(user=user).first()  # depends on your Review model

    context = {
        'product': product,
        'show_review_button': show_review_button,
        'existing_review': existing_review,
    }
    return render(request, 'store/product_detail.html', context)
