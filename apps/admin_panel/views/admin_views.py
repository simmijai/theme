# admin_panel/views/admin_views.py
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from apps.products.models import Category


from django.shortcuts import redirect

def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == 'admin':
            return view_func(request, *args, **kwargs)
        return redirect('admin_login')  # your login URL name
    return wrapper

@admin_required
def admin_dashboard(request):
    return render(request, 'admin/dashboard.html')




# def admin_subcategory_list(request):
#     return render(request, 'admin/categories/subcategory.html')

def admin_subcategory_list(request, category_id):
    # fetch the parent category
    category = get_object_or_404(Category, id=category_id)
    # fetch subcategories
    subcategories = category.subcategories.all()

    return render(request, 'admin/categories/subcategory.html', {
        'category': category,
        'subcategories': subcategories
    })

def customer_details(request):
    return render(request, 'admin/customers/customer_details.html')


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
                return render(request, 'admin/admin_login.html', {'error': 'You are not authorized as admin.'})
        else:
            return render(request, 'admin/admin_login.html', {'error': 'Invalid credentials.'})

    return render(request, 'admin/admin_login.html', {'error': 'Invalid credentials.'})
