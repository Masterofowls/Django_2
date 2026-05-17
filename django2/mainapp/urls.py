from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("products/", views.ProductListView.as_view(), name="product_list"),
    path("products/partial/", views.product_list_partial, name="product_list_partial"),
    path("products/create/", views.ProductCreateView.as_view(), name="product_create"),
]
