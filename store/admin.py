"""
Store Admin Configuration
Customizes the admin interface for Categories and Products
"""

from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Admin interface for Category model
    """
    list_display = ['name', 'slug', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']
    list_filter = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'
    ordering = ['name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Admin interface for Product model with advanced features
    """
    list_display = [
        'name', 
        'category', 
        'price', 
        'discounted_price', 
        'stock', 
        'available', 
        'featured',
        'created_at'
    ]
    list_filter = ['available', 'featured', 'category', 'created_at', 'updated_at']
    list_editable = ['price', 'stock', 'available', 'featured']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('category', 'name', 'slug', 'description')
        }),
        ('Pricing', {
            'fields': ('price', 'discounted_price')
        }),
        ('Inventory', {
            'fields': ('stock', 'available')
        }),
        ('Media', {
            'fields': ('image',)
        }),
        ('Additional Options', {
            'fields': ('featured',),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['make_available', 'make_unavailable', 'mark_as_featured']
    
    def make_available(self, request, queryset):
        """Bulk action to make products available"""
        updated = queryset.update(available=True)
        self.message_user(request, f'{updated} products marked as available.')
    make_available.short_description = "Mark selected products as available"
    
    def make_unavailable(self, request, queryset):
        """Bulk action to make products unavailable"""
        updated = queryset.update(available=False)
        self.message_user(request, f'{updated} products marked as unavailable.')
    make_unavailable.short_description = "Mark selected products as unavailable"
    
    def mark_as_featured(self, request, queryset):
        """Bulk action to mark products as featured"""
        updated = queryset.update(featured=True)
        self.message_user(request, f'{updated} products marked as featured.')
    mark_as_featured.short_description = "Mark selected products as featured"