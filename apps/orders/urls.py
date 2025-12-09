from django.urls import path
from . import views

urlpatterns = [
    path('checkout/', views.checkout, name='orders_checkout'),
    
    path('address/delete/<int:pk>/', views.delete_address, name='delete_address'),


    path('payment/', views.payment_page, name='payment_page'),
    path('place_order/', views.place_order, name='place_order'),
    path('my-orders/', views.my_orders, name='my_orders'),
]


