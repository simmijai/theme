# admin_panel/views/admin_views.py
from django.shortcuts import render,get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView
from apps.accounts.models import Account, Address
from apps.orders.models import Order
from django.db.models import Max, Count

from django.db.models import Subquery, OuterRef

class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return True  # Temporarily allow all users for testing



class AdminCustomerListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = Account
    template_name = 'admin_theme/customers/customer_list.html'
    context_object_name = 'customers'
    paginate_by = 25
    
    def get_queryset(self):
        customers = Account.objects.filter(role='customer').prefetch_related('addresses', 'order_set').annotate(
            total_orders=Count('order'),
            last_order_date=Max('order__created_at')
        ).order_by('-date_joined')
        
        # Add latest order to each customer
        for customer in customers:
            customer.latest_order = customer.order_set.first() if customer.order_set.exists() else None
        
        return customers

# Keep FBV for backward compatibility
def customer_list(request):
     # Get all customers with addresses and latest order
    customers = Account.objects.filter(role='customer').prefetch_related('addresses', 'order_set').annotate(
        total_orders=Count('order'),                # total orders per customer
        last_order_date=Max('order__created_at')    # latest order date per customer
    )
    
    # Add latest order to each customer
    for customer in customers:
        customer.latest_order = customer.order_set.first() if customer.order_set.exists() else None
    
    return render(request, 'admin_theme/customers/customer_list.html', {'customers': customers})


def customer_details(request, customer_id):
    customer = get_object_or_404(Account, id=customer_id)

    # Fetch orders
    orders = Order.objects.filter(user=customer).order_by('-created_at')

    # Get latest order for address info
    customer.latest_order = orders.first() if orders.exists() else None

    # Annotate extra info
    for order in orders:
        order.products_count = order.items.count()
        order.total_amount = order.total_price
        order.date = order.created_at

    # Customer extra info
    customer.total_orders = orders.count()
    customer.last_order_date = orders.first().created_at if orders.exists() else None

    context = {
        'customer': customer,
        'customer_orders': orders,
    }

    return render(request, 'admin_theme/customers/customer_details.html', context)
