from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView
from django.db.models import Q
from apps.orders.models import Order
from django.views.decorators.http import require_POST

class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return True  # Temporarily allow all users for testing

class AdminOrderListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = Order
    template_name = 'admin_theme/orders/order_list.html'
    context_object_name = 'orders'
    paginate_by = 5
    
    def get_queryset(self):
        queryset = Order.objects.select_related('user').prefetch_related('items__product')
        
        # Filter by status
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        
        # Search by customer name or email
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(user__first_name__icontains=search) |
                Q(user__last_name__icontains=search) |
                Q(user__email__icontains=search)
            )
        
        # Filter by payment method
        payment = self.request.GET.get('payment')
        if payment:
            queryset = queryset.filter(payment_method=payment)
        
        return queryset.order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_choices'] = Order.STATUS_CHOICES
        context['search'] = self.request.GET.get('search', '')
        context['status'] = self.request.GET.get('status', '')
        context['payment'] = self.request.GET.get('payment', '')
        return context

# Keep FBV for backward compatibility
def admin_order_list(request):
    orders = Order.objects.select_related('user').prefetch_related('items__product').order_by('-created_at')
    return render(request, 'admin_theme/orders/order_list.html', {'orders': orders})

from django.views.decorators.http import require_POST

@require_POST
def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    new_status = request.POST.get('status', '').strip()
    
    # Validate status against allowed choices
    valid_statuses = [choice[0] for choice in Order.STATUS_CHOICES]
    if new_status in valid_statuses:
        order.status = new_status
        order.save()
    
    # Safely redirect back
    next_url = request.META.get('HTTP_REFERER')
    if next_url and next_url.startswith(request.build_absolute_uri('/')):
        return redirect(next_url)
    return redirect('admin_order_list')


def order_detail(request, order_id):
    try:
        order = get_object_or_404(Order, id=order_id)

        # Annotate subtotal for template with error handling
        try:
            for item in order.items.all():
                item.subtotal = (item.quantity or 0) * (item.price or 0)
        except Exception:
            messages.warning(request, 'Error calculating item subtotals.')

        context = {
            'order': order
        }
        return render(request, 'admin_theme/orders/order_detail.html', context)
    except Exception as e:
        messages.error(request, 'Error loading order details. Please try again.')
        return redirect('admin_order_list')
