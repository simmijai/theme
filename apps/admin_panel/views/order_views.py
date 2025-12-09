from django.shortcuts import render, redirect, get_object_or_404
from apps.orders.models import Order
from django.views.decorators.http import require_POST

def admin_order_list(request):
    orders = Order.objects.select_related('user').prefetch_related('items__product').order_by('-created_at')
    return render(request, 'admin_theme/orders/order_list.html', {'orders': orders})

from django.views.decorators.http import require_POST

@require_POST
def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    new_status = request.POST.get('status')
    if new_status in dict(Order.STATUS_CHOICES).keys():
        order.status = new_status
        order.save()
    # redirect back to the same page if coming from detail
    next_url = request.META.get('HTTP_REFERER', 'admin_order_list')
    return redirect(next_url)


def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    # Optional: annotate subtotal for template
    for item in order.items.all():
        item.subtotal = item.quantity * item.price

    context = {
        'order': order
    }
    return render(request, 'admin_theme/orders/order_detail.html', context)
