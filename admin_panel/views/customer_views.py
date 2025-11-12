# admin_panel/views/admin_views.py
from django.shortcuts import render


def customer_details(request):
    return render(request, 'admin/customer_details.html')

def customer_list(request):
    return render(request, 'admin/customer_list.html')
