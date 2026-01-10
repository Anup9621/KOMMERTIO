"""
Orders Admin Configuration
Customizes admin interface for managing orders
"""

from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    """
    Inline admin for OrderItem - allows editing items within order page
    """
    model = OrderItem
    raw_id_fields = ['product']
    extra = 0
    readonly_fields = ['price', 'get_cost']
    
    def get_cost(self, obj):
        """Display total cost for this item"""
        return f'${obj.get_cost()}'
    get_cost.short_description = 'Total'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """
    Admin interface for Order model with inline items
    """
    list_display = [
        'id',
        'user',
        'email',
        'total_amount',
        'status',
        'payment_status',
        'created_at'
    ]
    list_filter = ['status', 'payment_status', 'created_at', 'updated_at']
    search_fields = ['id', 'user__username', 'email', 'first_name', 'last_name']
    list_editable = ['status', 'payment_status']
    inlines = [OrderItemInline]
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at', 'updated_at', 'payment_id']
    
    fieldsets = (
        ('Order Information', {
            'fields': ('user', 'status', 'payment_status', 'payment_id', 'total_amount')
        }),
        ('Customer Details', {
            'fields': ('first_name', 'last_name', 'email', 'phone')
        }),
        ('Shipping Address', {
            'fields': ('address', 'city', 'state', 'postal_code', 'country')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_as_processing', 'mark_as_shipped', 'mark_as_delivered']
    
    def mark_as_processing(self, request, queryset):
        """Bulk action to mark orders as processing"""
        updated = queryset.update(status='processing')
        self.message_user(request, f'{updated} orders marked as processing.')
    mark_as_processing.short_description = "Mark selected orders as processing"
    
    def mark_as_shipped(self, request, queryset):
        """Bulk action to mark orders as shipped"""
        updated = queryset.update(status='shipped')
        self.message_user(request, f'{updated} orders marked as shipped.')
    mark_as_shipped.short_description = "Mark selected orders as shipped"
    
    def mark_as_delivered(self, request, queryset):
        """Bulk action to mark orders as delivered"""
        updated = queryset.update(status='delivered')
        self.message_user(request, f'{updated} orders marked as delivered.')
    mark_as_delivered.short_description = "Mark selected orders as delivered"