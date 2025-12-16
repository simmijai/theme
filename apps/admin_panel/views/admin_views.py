# admin_panel/views/admin_views.py
from django.shortcuts import render, get_object_or_404
from apps.products.models import Category
from functools import wraps



from django.shortcuts import redirect

def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('admin_login')
        if request.user.role != 'admin':
            return redirect('admin_login')
        return view_func(request, *args, **kwargs)
    return wrapper


from django.db.models import Count, Sum, Avg
from apps.products.models import Product
from apps.accounts.models import Account
from apps.orders.models import Order
from apps.store.models import Review
from datetime import datetime, timedelta

@admin_required
def admin_dashboard(request):
    # Get dashboard statistics
    total_products = Product.objects.count()
    total_customers = Account.objects.filter(role='customer').count()
    total_orders = Order.objects.count()
    total_revenue = Order.objects.filter(status='delivered').aggregate(Sum('total_price'))['total_price__sum'] or 0
    
    # Recent orders
    recent_orders = Order.objects.select_related('user').order_by('-created_at')[:5]
    
    # Low stock products
    low_stock_products = Product.objects.filter(stock__lte=10).order_by('stock')[:5]
    
    # Recent reviews
    recent_reviews = Review.objects.select_related('product', 'user').order_by('-created_at')[:5]
    
    # Monthly stats (last 30 days)
    last_30_days = datetime.now() - timedelta(days=30)
    monthly_orders = Order.objects.filter(created_at__gte=last_30_days).count()
    monthly_revenue = Order.objects.filter(created_at__gte=last_30_days, status='delivered').aggregate(Sum('total_price'))['total_price__sum'] or 0
    
    context = {
        'total_products': total_products,
        'total_customers': total_customers,
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'recent_orders': recent_orders,
        'low_stock_products': low_stock_products,
        'recent_reviews': recent_reviews,
        'monthly_orders': monthly_orders,
        'monthly_revenue': monthly_revenue,
    }
    return render(request, 'admin_theme/dashboard.html', context)


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from apps.accounts.models import Account

def admin_login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Authenticate user
        user = authenticate(request, email=email, password=password)

        if user is not None:
            if user.role == 'admin':
                login(request, user)
                return redirect('admin_dashboard')  # replace with your admin dashboard url
            else:
                return render(request, 'admin_theme/admin_login.html', {'error': 'You are not authorized as admin.'})
        else:
            return render(request, 'admin_theme/admin_login.html', {'error': 'Invalid credentials.'})

    return render(request, 'admin_theme/admin_login.html', {'error': 'Invalid credentials.'})


from django.contrib.auth import logout

def admin_logout(request):
    logout(request)
    return redirect('admin_login')  # redirect to admin login page

