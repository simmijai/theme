from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from products.models import Product
from .models import Wishlist

@login_required
def wishlist_view(request):
    """Display all wishlist items for the logged-in user."""
    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request, 'store/wishlist.html', {'wishlist_items': wishlist_items})


@login_required
def add_to_wishlist(request, product_id):
    """Add product to wishlist."""
    product = get_object_or_404(Product, id=product_id)

    # Check if product already in wishlist
    wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, product=product)

    if created:
        return JsonResponse({'success': True, 'message': 'Added to wishlist'})
    else:
        return JsonResponse({'success': False, 'message': 'Already in wishlist'})

@login_required
def remove_from_wishlist(request, product_id):
    """Remove a product from wishlist."""
    Wishlist.objects.filter(user=request.user, product_id=product_id).delete()
    return JsonResponse({'success': True, 'message': 'Removed from wishlist'})
