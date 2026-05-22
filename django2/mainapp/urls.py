from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("products/", views.ProductListView.as_view(), name="product_list"),
    path("products/partial/", views.product_list_partial, name="product_list_partial"),
    path("products/create/", views.ProductCreateView.as_view(), name="product_create"),
    path("products/<int:pk>/edit/",views.ProductUpdateView.as_view(),name="product_update",),
    path("products/<int:pk>/delete/", views.product_delete_view, name="product_delete"),
    path("products/<int:pk>/cancel/",views.product_cancel_edit,name="product_cancel_edit",),
    path("cart/", views.cart_view, name="cart"),
    path("cart/add/<int:pk>/", views.cart_add, name="cart_add"),
    path("cart/remove/<int:pk>/", views.cart_remove, name="cart_remove"),
    path("orders/", views.OrderListView.as_view(), name="order_list"),
]
