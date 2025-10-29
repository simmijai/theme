from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse

def login(request):
    return render(request,'accounts/login.html')

def register(request):
    return render(request,'accounts/register.html')