from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('verify-email/<uuid:token>/', views.verify_email, name='verify_email'),
    path('login/', views.login_view, name='login'),
    path('login_otp/', views.login_otp_view, name='login_otp'),
    
    path('accounts/logout/', LogoutView.as_view(next_page='/'), name='logout'),
    

]
