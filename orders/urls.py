"""
Orders URL Configuration
Maps URLs to order and checkout views
"""

from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    # Checkout and payment
    path('checkout/', views.checkout, name='checkout'),
    path('payment/', views.payment, name='payment'),
    path('payment/success/<int:order_id>/', views.payment_success, name='payment_success'),
    path('payment/failed/', views.payment_failed, name='payment_failed'),
    
    # Order history
    path('history/', views.order_history, name='order_history'),
    path('detail/<int:order_id>/', views.order_detail, name='order_detail'),
]