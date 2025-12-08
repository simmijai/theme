from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.products.models import Product
from .models import CartItem
from django.http import JsonResponse



@login_required
def add_to_cart(request, product_id):
    """Add product to user's cart or increase quantity if already exists"""
    try:
        product = get_object_or_404(Product, id=product_id)
        
        # Handle both POST and GET requests
        if request.method == 'POST':
            quantity = int(request.POST.get('quantity', 1))
        else:
            quantity = int(request.GET.get('quantity', 1))
        
        # Validate quantity
        if quantity < 1:
            quantity = 1
        
        cart_item, created = CartItem.objects.get_or_create(
            user=request.user,
            product=product,
            defaults={'quantity': quantity}
        )

        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        messages.success(request, f"'{product.name}' added to your cart.")
        return redirect('cart_view')
    
    except ValueError:
        messages.error(request, 'Invalid quantity provided.')
        return redirect('cart_view')
    except Exception as e:
        messages.error(request, f'Error adding item to cart: {str(e)}')
        return redirect('cart_view')


@login_required
def cart_view(request):
    """Display all cart items of logged-in user"""
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.total_price() for item in cart_items)

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'user_theme/store/cart2.html', context)


@login_required
def remove_from_cart(request, product_id):
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, user=request.user, product_id=product_id)
        cart_item.delete()
        return JsonResponse({'success': True, 'message': 'Item removed from cart'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)


@login_required
def update_quantity(request, product_id):
    """Update the quantity for a cart item via AJAX. Expects POST with 'quantity'."""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=400)

    try:
        qty = int(request.POST.get('quantity', 1))
    except (TypeError, ValueError):
        return JsonResponse({'success': False, 'message': 'Invalid quantity'}, status=400)

    if qty < 1:
        # Treat quantities less than 1 as removal
        cart_item = CartItem.objects.filter(user=request.user, product_id=product_id).first()
        if cart_item:
            cart_item.delete()
        # compute totals
        cart_items = CartItem.objects.filter(user=request.user)
        cart_total = sum(item.total_price() for item in cart_items)
        return JsonResponse({'success': True, 'message': 'Item removed', 'cart_total': cart_total})

    cart_item = CartItem.objects.filter(user=request.user, product_id=product_id).first()
    if not cart_item:
        return JsonResponse({'success': False, 'message': 'Cart item not found'}, status=404)

    cart_item.quantity = qty
    cart_item.save()

    # recompute totals
    item_total = cart_item.total_price()
    cart_items = CartItem.objects.filter(user=request.user)
    cart_total = sum(item.total_price() for item in cart_items)

    return JsonResponse({
        'success': True,
        'message': 'Quantity updated',
        'item_total': item_total,
        'cart_total': cart_total,
        'quantity': cart_item.quantity,
    })
