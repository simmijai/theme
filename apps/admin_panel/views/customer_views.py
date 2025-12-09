# admin_panel/views/admin_views.py
from django.shortcuts import render,get_object_or_404
from apps.accounts.models import Account, Address
from apps.orders.models import Order
from django.db.models import Max, Count





def customer_list(request):
     # Get all customers
    customers = Account.objects.filter(role='customer').annotate(
        total_orders=Count('order'),                # total orders per customer
        last_order_date=Max('order__created_at')    # latest order date per customer
    )
    return render(request, 'admin_theme/customers/customer_list.html', {'customers': customers})


def customer_details(request, customer_id):
    customer = get_object_or_404(Account, id=customer_id)

    # Fetch orders
    orders = Order.objects.filter(user=customer).order_by('-created_at')

    # Annotate extra info
    for order in orders:
        order.products_count = order.items.count()
        order.total_amount = order.total_price
        order.date = order.created_at

    # Customer extra info
    customer.total_orders = orders.count()
    customer.last_order_date = orders.first().created_at if orders.exists() else None

    # Prepare address string
    addresses = customer.addresses.all()  # Make sure your Account model has a related_name 'addresses'
    customer.address = ", ".join([f"{a.address_line1}, {a.city}" for a in addresses])

    context = {
        'customer': customer,
        'customer_orders': orders,  # ✅ This is what template loops over
    }

    return render(request, 'admin_theme/customers/customer_details.html', context)
