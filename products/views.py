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



# def subcategory_products(request, slug):
#     subcategory = get_object_or_404(Category, slug=slug, parent__isnull=False)  # ensures it's a subcategory
#     products = Product.objects.filter(category=subcategory)  # adjust field if needed

#     context = {
#         'products': products,
#         'top_categories': Category.objects.filter(parent=None),  # navbar
#     }
#     return render(request, 'store/product_subcategory.html', context)

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
        # Example: Assuming you have an OrderItem model or sales count field
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


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'store/product_detail.html', {'product': product})

