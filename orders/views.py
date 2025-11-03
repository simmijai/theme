from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from cart.models import CartItem

@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.total_price() for item in cart_items)
    shipping_cost = 50  # static for now

    return render(request, 'store/checkout.html', {
        'cart_items': cart_items,
        'total_price': total_price + shipping_cost,
        'shipping_cost': shipping_cost
    })
