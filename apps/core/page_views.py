from django.shortcuts import render

def about_us(request):
    return render(request, 'user_theme/pages/about.html')

def payment_policy(request):
    return render(request, 'user_theme/pages/payment_policy.html')

def terms_conditions(request):
    return render(request, 'user_theme/pages/terms_conditions.html')

def return_refund(request):
    return render(request, 'user_theme/pages/return_refund.html')

def shipping_policy(request):
    return render(request, 'user_theme/pages/shipping_policy.html')

def warranty(request):
    return render(request, 'user_theme/pages/warranty.html')