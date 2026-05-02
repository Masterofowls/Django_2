from django.contrib import admin
from .models import Product
# Register your models here.

@admin.register(Product)

class ProductAdmin(admin.ModelAdmin):
  list_display = ('id', 'article', 'name', 'category', 'manufacturer', 'price', 'supplier', 'stock_quantity')
  list_filter = ('category', 'manufacturer', 'price', 'stock_quantity', 'supplier')
  search_fields = ('name', 'article', 'description')
