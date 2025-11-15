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



from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from products.models import Product
from store.models import Review
from orders.models import Order

@login_required
def add_or_edit_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    user = request.user

    # Try to get existing review
    review, created = Review.objects.get_or_create(
        product=product,
        user=user,
        defaults={'order': Order.objects.filter(user=user, status='Delivered').last()}
    )

    # Only allow review if user has a delivered order for this product
    delivered_orders = product.orderitem_set.filter(order__user=user, order__status='Delivered')
    if not delivered_orders.exists():
        messages.error(request, "You cannot review a product you haven't purchased.")
        return redirect('product_detail', slug=product.slug)

    if request.method == "POST":
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        image = request.FILES.get('image')

        review.rating = rating
        review.comment = comment
        if image:
            review.image = image
        review.save()

        messages.success(request, "Your review has been submitted successfully!")
        return redirect('product_detail', slug=product.slug)

    # GET request is handled by the modal already, no need to render separate template
    return redirect('product_detail', slug=product.slug)



@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    product_slug = review.product.slug
    review.delete()
    return redirect('product_detail', slug=product_slug)
