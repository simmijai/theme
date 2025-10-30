# admin_panel/views/admin_views.py
from django.shortcuts import render

def admin_dashboard(request):
    return render(request, 'admin/dashboard.html')

def admin_product(request):
    return render(request, 'admin/product.html')

def admin_product_create(request):
    return render(request, 'admin/product_create.html')

def admin_subcategory_list(request):
    return render(request, 'admin/subcategory.html')

def customer_details(request):
    return render(request, 'admin/customer_details.html')
