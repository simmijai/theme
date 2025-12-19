from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from django.urls import reverse
from apps.products.models import Product
from .models import Wishlist

@login_required
def wishlist_view(request):
    """Display all wishlist items for the logged-in user."""
    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request, 'user_theme/store/wishlist.html', {'wishlist_items': wishlist_items})


@login_required
def add_to_wishlist(request, product_id):
    """Add product to wishlist."""
    product = get_object_or_404(Product, id=product_id)

    # Check if product already in wishlist
    wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, product=product)

    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'

    if is_ajax:
        if created:
            return JsonResponse({'success': True, 'message': 'Added to wishlist'})
        else:
            return JsonResponse({'success': False, 'message': 'Already in wishlist'})
    else:
        # Non-AJAX: use messages and redirect back to referring page (or wishlist)
        if created:
            messages.success(request, 'Product added to your wishlist.')
        else:
            messages.info(request, 'Product is already in your wishlist.')

        redirect_to = request.META.get('HTTP_REFERER') or reverse('wishlist')
        return redirect(redirect_to)

@login_required
def remove_from_wishlist(request, product_id):
    """Remove a product from wishlist."""
    wishlist_item = Wishlist.objects.filter(user=request.user, product_id=product_id)
    deleted_count = wishlist_item.delete()[0]  # delete() returns tuple (count, dict)

    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
    if is_ajax:
        if deleted_count > 0:
            return JsonResponse({'success': True, 'message': 'Removed from wishlist'})
        else:
            return JsonResponse({'success': False, 'message': 'Item not found'})
    else:
        messages.success(request, 'Product removed from your wishlist.')
        redirect_to = request.META.get('HTTP_REFERER') or reverse('wishlist')
        return redirect(redirect_to)

