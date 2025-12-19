from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from apps.cart.models import CartItem
from apps.accounts.models import Address
from apps.accounts.forms import AddressForm
from .models import Order

@login_required
def checkout(request):
    user = request.user

    cart_items = CartItem.objects.filter(user=user)
    
    # Check if cart is empty
    if not cart_items.exists():
        messages.error(request, "Your cart is empty. Add items before checkout.")
        return redirect('cart_view')
    
    total_price = sum(item.total_price() for item in cart_items)

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
    # HANDLE ADDRESS SELECTION
    # --------------------------
    if request.method == "POST" and 'selected_address' in request.POST:
        selected_address_id = request.POST.get('selected_address')
        request.session['selected_address_id'] = selected_address_id
        messages.success(request, 'Address selected successfully.')
        return redirect('payment_page')  # Redirect to payment page
    
    # --------------------------
    # ADD / EDIT ADDRESS  
    # --------------------------
    elif request.method == "POST":
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
            messages.success(request, "Address added successfully.")
            return redirect("orders_checkout")
        else:
            # Print errors for debugging
            print("Form errors:", form.errors)
    else:
        form = AddressForm()

    return render(request, 'user_theme/store/checkout.html', {
        "addresses": addresses,
        "form": form,
        "cart_items": cart_items,
        "total_price": total_price,
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
    
    # Check if cart is empty
    if not cart_items.exists():
        messages.error(request, "Your cart is empty. Add items before proceeding to payment.")
        return redirect('cart_view')
    
    total_price = sum(item.total_price() for item in cart_items)
    grand_total = total_price
    return render(request, 'user_theme/store/payment.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'grand_total': grand_total,
    })


@login_required
def place_order(request):
    if request.method == "POST":
        payment_method = request.POST.get("payment_method", "COD")
        cart_items = CartItem.objects.filter(user=request.user)
        
        # Check if cart is empty
        if not cart_items.exists():
            messages.error(request, "Your cart is empty. Cannot place order.")
            return redirect('cart_view')
        
        total_price = sum(item.total_price() for item in cart_items)

        # Get selected address from session or default
        selected_address_id = request.session.get('selected_address_id')
        address = None
        if selected_address_id:
            try:
                address = Address.objects.get(id=selected_address_id, user=request.user)
            except Address.DoesNotExist:
                pass
        
        if not address:
            address = Address.objects.filter(user=request.user).first()
        
        if not address:
            messages.error(request, 'Please add a delivery address before placing order.')
            return redirect('orders_checkout')
        
        # ✅ create order with shipping address fields
        order = Order.objects.create(
            user=request.user,
            shipping_first_name=address.first_name,
            shipping_last_name=address.last_name,
            shipping_phone=address.phone,
            shipping_address_line1=address.address_line1,
            shipping_city=address.city,
            shipping_state=address.state,
            shipping_country=address.country,
            shipping_postal_code=address.postal_code,
            shipping_landmark=address.near_by_landmark,
            total_price=total_price,
            payment_method=payment_method,
            status="Pending"
        )

        # ✅ create each order item and update stock
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )
            # Update stock
            item.product.stock -= item.quantity
            item.product.save()

        # ✅ clear cart
        cart_items.delete()

        # ✅ redirect to "my orders" page
        return redirect('my_orders')

    return redirect('payment_page')



from apps.core.pagination import GlobalPaginator

@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).prefetch_related('items__product').order_by('-created_at')
    
    # Add pagination
    pagination_data = GlobalPaginator.paginate(orders, request, 10)
    
    return render(request, 'user_theme/store/my_orders.html', {
        'orders': pagination_data['page_obj'].object_list,
        **pagination_data
    })




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
