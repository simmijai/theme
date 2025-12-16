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
    try:
        # Get dashboard statistics with error handling
        total_products = Product.objects.count() or 0
        total_customers = Account.objects.filter(role='customer').count() or 0
        total_orders = Order.objects.count() or 0
        
        # Safe revenue calculation
        try:
            revenue_data = Order.objects.filter(status='delivered').aggregate(Sum('total_price'))
            total_revenue = revenue_data['total_price__sum'] or 0
        except Exception:
            total_revenue = 0
        
        # Recent orders with error handling
        try:
            recent_orders = Order.objects.select_related('user').order_by('-created_at')[:5]
        except Exception:
            recent_orders = []
        
        # Low stock products with error handling
        try:
            low_stock_products = Product.objects.filter(stock__lte=10).order_by('stock')[:5]
        except Exception:
            low_stock_products = []
        
        # Recent reviews with error handling
        try:
            recent_reviews = Review.objects.select_related('product', 'user').order_by('-created_at')[:5]
        except Exception:
            recent_reviews = []
        
        # Monthly stats with error handling
        try:
            last_30_days = datetime.now() - timedelta(days=30)
            monthly_orders = Order.objects.filter(created_at__gte=last_30_days).count() or 0
            monthly_revenue_data = Order.objects.filter(created_at__gte=last_30_days, status='delivered').aggregate(Sum('total_price'))
            monthly_revenue = monthly_revenue_data['total_price__sum'] or 0
        except Exception:
            monthly_orders = 0
            monthly_revenue = 0
        
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
        
    except Exception as e:
        # Log the error and show user-friendly message
        messages.error(request, 'Error loading dashboard data. Please try again.')
        # Return minimal context to prevent template errors
        context = {
            'total_products': 0,
            'total_customers': 0,
            'total_orders': 0,
            'total_revenue': 0,
            'recent_orders': [],
            'low_stock_products': [],
            'recent_reviews': [],
            'monthly_orders': 0,
            'monthly_revenue': 0,
        }
        return render(request, 'admin_theme/dashboard.html', context)


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from apps.accounts.models import Account
from apps.admin_panel.forms import AdminLoginForm

def admin_login(request):
    if request.method == "POST":
        form = AdminLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            # Authenticate user
            user = authenticate(request, email=email, password=password)
            
            if user is not None:
                if user.role == 'admin':
                    login(request, user)
                    messages.success(request, f'Welcome back, {user.first_name}!')
                    return redirect('admin_dashboard')
                else:
                    form.add_error(None, 'You are not authorized as admin.')
            else:
                form.add_error(None, 'Invalid email or password.')
        
        # Form has errors
        return render(request, 'admin_theme/admin_login.html', {'form': form})
    else:
        form = AdminLoginForm()
    
    return render(request, 'admin_theme/admin_login.html', {'form': form})


from django.contrib.auth import logout

def admin_logout(request):
    logout(request)
    return redirect('admin_login')  # redirect to admin login page

