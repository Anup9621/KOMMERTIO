"""
Main URL Configuration for E-commerce Project
Includes all app URLs and media/static file serving
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Admin panel
    path('admin/', admin.site.urls),
    
    # App URLs
    path('', include('store.urls')),  # Store URLs (home, products, etc.)
    path('accounts/', include('accounts.urls')),  # User authentication URLs
    path('cart/', include('cart.urls')),  # Shopping cart URLs
    path('orders/', include('orders.urls')),  # Orders and checkout URLs
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Customize admin site headers
admin.site.site_header = "E-commerce Admin"
admin.site.site_title = "E-commerce Admin Portal"
admin.site.index_title = "Welcome to E-commerce Admin Panel"