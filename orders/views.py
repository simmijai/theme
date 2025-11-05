from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from cart.models import CartItem
from accounts.models import Address
from accounts.forms import AddressForm
from .models import Order


@login_required
def checkout(request):
    user = request.user
    cart_items = CartItem.objects.filter(user=user)
    total_price = sum(item.total_price() for item in cart_items)
    shipping_cost = 50

    addresses = Address.objects.filter(user=user)

    if request.method == "POST":
        # Handle selecting an existing address
        selected_address_id = request.POST.get("selected_address")
        if selected_address_id:
            selected_address = Address.objects.get(id=selected_address_id, user=user)
            # Save selected_address to order here
            return redirect('orders_checkout')
        else:
            # Handle new address submission
            form = AddressForm(request.POST)
            if form.is_valid():
                address = form.save(commit=False)
                address.user = user
                if not addresses.exists():
                    address.is_default = True
                address.save()
                return redirect('orders_checkout')
    else:
        form = AddressForm()

    return render(request, 'store/checkout.html', {
        'cart_items': cart_items,
        'total_price': total_price + shipping_cost,
        'shipping_cost': shipping_cost,
        'addresses': addresses,
        'form': form,
    })

