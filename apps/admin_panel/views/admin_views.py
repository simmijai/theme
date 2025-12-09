# admin_panel/views/admin_views.py
from django.shortcuts import render
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


@admin_required
def admin_dashboard(request):
    return render(request, 'admin_theme/dashboard.html')


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

