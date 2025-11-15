# admin_panel/views/admin_views.py
from django.shortcuts import render

def admin_dashboard(request):
    return render(request, 'admin/dashboard.html')




def admin_subcategory_list(request):
    return render(request, 'admin/categories/subcategory.html')

def customer_details(request):
    return render(request, 'admin/customers/customer_details.html')
