from django.contrib import admin
from .models import Product, Category, Manufacturer, Supplier, PickUpPoint, Order


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "article",
        "name",
        "category",
        "manufacturer",
        "price",
        "supplier",
        "stock_quantity",
    )
    list_filter = ("category", "manufacturer", "price", "stock_quantity", "supplier")
    search_fields = ("name", "article", "description")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_filter = ("name",)
    search_fields = ("name",)


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_filter = ("name",)
    search_fields = ("name",)


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_filter = ("name",)
    search_fields = ("name",)


@admin.register(PickUpPoint)
class PickUpPointAdmin(admin.ModelAdmin):
    list_display = ("id", "address")  # ← поле address, а не name
    list_filter = ("address",)  # ← опционально
    search_fields = ("address",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "number",
        "order_date",
        "delivery_date",
        "pickup_point",
        "status",
    )
    list_filter = ("status", "order_date", "delivery_date")
    search_fields = ("number",)
