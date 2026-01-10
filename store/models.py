"""
Store Models
Defines Category and Product models for the e-commerce store
"""

from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Category(models.Model):
    """
    Category model for organizing products
    """
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Categories'
    
    def save(self, *args, **kwargs):
        """Auto-generate slug from name if not provided"""
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        """Return URL for category detail page"""
        return reverse('store:category_products', kwargs={'slug': self.slug})


class Product(models.Model):
    """
    Product model with pricing, inventory, and category relationship
    """
    category = models.ForeignKey(
        Category, 
        related_name='products', 
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discounted_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        blank=True, 
        null=True,
        help_text="Optional discounted price"
    )
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)
    available = models.BooleanField(default=True)
    featured = models.BooleanField(default=False, help_text="Show on homepage")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['available', '-created_at']),
        ]
    
    def save(self, *args, **kwargs):
        """Auto-generate slug from name if not provided"""
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        """Return URL for product detail page"""
        return reverse('store:product_detail', kwargs={'slug': self.slug})
    
    def get_price(self):
        """Return discounted price if available, otherwise regular price"""
        if self.discounted_price:
            return self.discounted_price
        return self.price
    
    def get_discount_percentage(self):
        """Calculate discount percentage if discounted price exists"""
        if self.discounted_price and self.discounted_price < self.price:
            discount = ((self.price - self.discounted_price) / self.price) * 100
            return round(discount)
        return 0
    
    def is_in_stock(self):
        """Check if product is in stock"""
        return self.stock > 0 and self.available