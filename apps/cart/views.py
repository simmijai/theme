from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.products.models import Product
from .models import CartItem
from django.http import JsonResponse



@login_required
def add_to_cart(request, product_id):
    """Add product to user's cart or increase quantity if already exists"""
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))

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



def remove_from_cart(request, product_id):
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, user=request.user, product_id=product_id)
        cart_item.delete()
        return JsonResponse({'success': True, 'message': 'Item removed from cart'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)
