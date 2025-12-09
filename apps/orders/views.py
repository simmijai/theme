from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from apps.cart.models import CartItem
from apps.accounts.models import Address
from apps.accounts.forms import AddressForm
from .models import Order

@login_required
def checkout(request):
    user = request.user

    cart_items = CartItem.objects.filter(user=user)
    total_price = sum(item.total_price() for item in cart_items)
    shipping_cost = 50

    addresses = Address.objects.filter(user=user)

    # --------------------------
    # DELETE ADDRESS  
    # --------------------------
    delete_id = request.GET.get("delete")
    if delete_id:
        Address.objects.filter(id=delete_id, user=user).delete()
        messages.success(request, "Address deleted successfully.")
        return redirect("orders_checkout")

    # --------------------------
    # ADD / EDIT ADDRESS  
    # --------------------------
    if request.method == "POST":
        edit_id = request.POST.get("address_id")  # Hidden field

        if edit_id:  
            # EDIT existing address
            address = get_object_or_404(Address, id=edit_id, user=user)
            form = AddressForm(request.POST, instance=address)
        else:
            # ADD new address
            form = AddressForm(request.POST)

        if form.is_valid():
            new_addr = form.save(commit=False)
            new_addr.user = user
            new_addr.save()
            return redirect("orders_checkout")

    else:
        form = AddressForm()

    return render(request, 'user_theme/store/checkout.html', {
        "addresses": addresses,
        "form": form,
        "cart_items": cart_items,
        "shipping_cost": shipping_cost,
        "total_price": total_price + shipping_cost,
    })

# @login_required
# def checkout(request):
#     user = request.user
#     cart_items = CartItem.objects.filter(user=user)
#     total_price = sum(item.total_price() for item in cart_items)
#     shipping_cost = 50

#     addresses = Address.objects.filter(user=user)

#     if request.method == "POST":
#         # Handle selecting an existing address
#         selected_address_id = request.POST.get("selected_address")
#         if selected_address_id:
#             selected_address = Address.objects.get(id=selected_address_id, user=user)
#             # Save selected_address to order here
#             return redirect('orders_checkout')
#         else:
#             # Handle new address submission
#             form = AddressForm(request.POST)
#             if form.is_valid():
#                 address = form.save(commit=False)
#                 address.user = user
#                 if not addresses.exists():
#                     address.is_default = True
#                 address.save()
#                 return redirect('orders_checkout')
#     else:
#         form = AddressForm()

#     return render(request, 'user_theme/store/checkout.html', {
#         'cart_items': cart_items,
#         'total_price': total_price + shipping_cost,
#         'shipping_cost': shipping_cost,
#         'addresses': addresses,
#         'form': form,
#     })

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Order, OrderItem

@login_required
def payment_page(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.total_price() for item in cart_items)
    shipping_cost = 50
    grand_total = total_price + shipping_cost
    return render(request, 'user_theme/store/payment.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'shipping_cost': shipping_cost,
        'grand_total': grand_total,
    })


@login_required
def place_order(request):
    if request.method == "POST":
        payment_method = request.POST.get("payment_method", "COD")
        cart_items = CartItem.objects.filter(user=request.user)
        total_price = sum(item.total_price() for item in cart_items)
        shipping_cost = 50

        # ✅ create order
        order = Order.objects.create(
            user=request.user,
            total_price=total_price + shipping_cost,
            payment_method=payment_method,
            status="Pending"  # must match your model choices
        )

        # ✅ create each order item (REMOVED subtotal)
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

        # ✅ clear cart
        cart_items.delete()

        # ✅ redirect to "my orders" page
        return redirect('my_orders')

    return redirect('payment_page')



@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).prefetch_related('items__product').order_by('-created_at')
    return render(request, 'user_theme/store/my_orders.html', {'orders': orders})


from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from apps.accounts.models import Address

from django.contrib import messages

@login_required
def delete_address(request, pk):
    address = get_object_or_404(Address, pk=pk, user=request.user)

    # restrict last remaining address
    if Address.objects.filter(user=request.user).count() == 1:
        messages.error(request, "You cannot delete the only address.")
        return redirect("orders_checkout")

    address.delete()

    # Fix default if needed
    remaining = Address.objects.filter(user=request.user)
    if not remaining.filter(is_default=True).exists():
        first = remaining.first()
        first.is_default = True
        first.save()

    # THIS IS WHAT TRIGGERS SWEETALERT
    messages.success(request, "Address deleted successfully.")

    return redirect("orders_checkout")
