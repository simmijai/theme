import random
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import Account
from django.contrib.auth import login as auth_login
import uuid
from apps.accounts.models import Address
from apps.accounts.forms import AddressForm
from django.contrib.auth.decorators import login_required
import threading
from .redis_otp import RedisOTPManager  # Import Redis manager

def send_otp_email_async(user_email, user_name, otp):
    """Send OTP email in background thread"""
    subject = 'Your Login OTP'
    message = f"""
    Hi {user_name},
    
    Your OTP for login is: {otp}
    
    This OTP is valid for 10 minutes.
    
    If you didn't request this, please ignore this email.
    """
    
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user_email],
        fail_silently=False,
    )

def register_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')

        if Account.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return redirect('register')

        username = email.split('@')[0]

        user = Account.objects.create_user(
            email=email,
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=None
        )
        user.is_active = False
        user.email_verified = False
        user.save()

        # unique token for verification
        token = str(uuid.uuid4())
        user.verification_token = token
        user.save()

        verification_link = f"http://127.0.0.1:8000/accounts/verify-email/{token}/"
        subject = 'Verify your email address'
        message = f'Hi {first_name},\n\nClick the link to verify your account:\n{verification_link}\n\nIf you did not register, ignore this email.'

        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email], fail_silently=False)
        messages.success(request, 'Registration successful! Check your email to verify your account.')
        return redirect('register')

    return render(request, 'user_theme/accounts/register.html')

def verify_email(request, token):
    try:
        user = Account.objects.get(verification_token=token)
        user.email_verified = True
        user.is_active = True
        user.verification_token = None
        user.save()
        messages.success(request, 'Email verified successfully! You can now log in.')
        return redirect('login')
    except Account.DoesNotExist:
        messages.error(request, 'Invalid or expired verification link.')
        return redirect('register')

# 🧩 Step 3: Login — Send OTP to verified email
def login_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        try:
            user = Account.objects.get(email=email)
            if not user.email_verified:
                messages.error(request, 'Email not verified. Please verify first.')
                return redirect('login')

            # ✅ USING REDIS - Generate OTP
            otp, error = RedisOTPManager.generate_otp(email)
            
            if error:
                messages.error(request, error)
                return redirect('login')

            # ✅ Send OTP email in background thread (faster)
            threading.Thread(
                target=send_otp_email_async,
                args=(email, user.first_name, otp)
            ).start()
            
            request.session['login_email'] = email
            messages.info(request, 'OTP sent to your email.')
            return redirect('login_otp')

        except Account.DoesNotExist:
            messages.error(request, 'No account found with that email.')

    return render(request, 'user_theme/accounts/login.html')


# 🧩 Step 4: Verify OTP for Login
def login_otp_view(request):
    email = request.session.get('login_email')
    if not email:
        messages.error(request, 'Session expired. Please login again.')
        return redirect('login')

    try:
        user = Account.objects.get(email=email)
    except Account.DoesNotExist:
        messages.error(request, 'Invalid session. Please try again.')
        return redirect('login')
    
    # Get remaining time - SIMPLE FIX
    remaining_seconds = 600  # Default 10 minutes
    
    try:
        rt = RedisOTPManager.get_remaining_time(email)
        if rt:
            remaining_seconds = rt
    except:
        pass  # Keep default if error


    if request.method == "POST":
        entered_otp = request.POST.get('otp')
         # ✅ USING REDIS - Verify OTP (super fast)
        is_valid, message = RedisOTPManager.verify_otp(email, entered_otp)
        
        if is_valid:
            # ✅ Cleanup OTP from Redis
            RedisOTPManager.cleanup_otp(email)
            
            user.otp = None  # Clear old DB OTP if exists
            user.save()
            auth_login(request, user)  # THIS logs the user in

            messages.success(request, f'Welcome {user.first_name}! Login successful.')
            return redirect('home')
        else:
            messages.error(request, 'Invalid OTP.')
            
        # Get remaining time for template
        remaining_time = RedisOTPManager.get_remaining_time(email)

    return render(request, 'user_theme/accounts/login_otp.html',
                  {
        'email': email,
        'remaining_seconds': remaining_seconds
                  })

@login_required
def edit_address(request, pk):
    address = get_object_or_404(Address, pk=pk, user=request.user)
    
    if request.method == "POST":
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            return redirect('orders_checkout')
    else:
        form = AddressForm(instance=address)
    
    return render(request, 'user_theme/accounts/edit_address.html', {'form': form})

@login_required
def delete_address(request, pk):
    address = get_object_or_404(Address, pk=pk, user=request.user)
    
    if request.method == "POST":
        address.delete()
        return redirect('orders_checkout')
    
    return render(request, 'user_theme/accounts/confirm_delete.html', {'address': address})

