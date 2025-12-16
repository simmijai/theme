# admin_panel/views/admin_views.py
from django.shortcuts import render,get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView
from django.db.models import Max, Count, Q
from apps.accounts.models import Account, Address
from apps.orders.models import Order

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
        queryset = Account.objects.filter(role='customer').prefetch_related('addresses', 'order_set').annotate(
            total_orders=Count('order'),
            last_order_date=Max('order__created_at')
        )
        
        # Search by name or email
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(email__icontains=search)
            )
        
        # Filter by order count
        orders = self.request.GET.get('orders')
        if orders == 'with_orders':
            queryset = queryset.filter(order__isnull=False).distinct()
        elif orders == 'no_orders':
            queryset = queryset.filter(order__isnull=True)
        
        customers = queryset.order_by('-date_joined')
        
        # Add latest order to each customer
        for customer in customers:
            customer.latest_order = customer.order_set.first() if customer.order_set.exists() else None
        
        return customers
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search', '')
        context['orders'] = self.request.GET.get('orders', '')
        return context

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
    try:
        customer = get_object_or_404(Account, id=customer_id)

        # Fetch orders with error handling
        try:
            orders = Order.objects.filter(user=customer).order_by('-created_at')
        except Exception:
            orders = Order.objects.none()
            messages.warning(request, 'Error loading customer orders.')

        # Get latest order for address info with error handling
        try:
            customer.latest_order = orders.first() if orders.exists() else None
        except Exception:
            customer.latest_order = None

        # Annotate extra info with error handling
        try:
            for order in orders:
                order.products_count = order.items.count() if hasattr(order, 'items') else 0
                order.total_amount = order.total_price or 0
                order.date = order.created_at
        except Exception:
            messages.warning(request, 'Error loading order details.')

        # Customer extra info with error handling
        try:
            customer.total_orders = orders.count() if orders else 0
            customer.last_order_date = orders.first().created_at if orders.exists() else None
        except Exception:
            customer.total_orders = 0
            customer.last_order_date = None

        context = {
            'customer': customer,
            'customer_orders': orders,
        }

        return render(request, 'admin_theme/customers/customer_details.html', context)
    except Exception as e:
        messages.error(request, 'Error loading customer details. Please try again.')
        return redirect('admin_customer_list')
