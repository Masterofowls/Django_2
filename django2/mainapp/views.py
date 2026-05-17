from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from .models import Product


def is_admin(user):
    """Возвращает True, если пользователь аутентифицирован и имеет роль admin."""
    return user.is_authenticated and user.role == "admin"


def home(request):
    return render(request, "mainapp/home.html")


class ProductListView(ListView):
    model = Product
    template_name = "mainapp/product_list.html"
    context_object_name = "products"


def product_list_partial(request):
    # возвращает html фрагмент
    products = Product.objects.select_related(
        "category", "manufacturer", "supplier"
    ).order_by("name")

    return render(
        request,
        "mainapp/_product_table.html",
        {"products": products},
    )


class ProductCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """Форма создания нового товара. Доступна только пользователям с ролью admin."""

    model = Product
    template_name = "mainapp/product_form.html"
    fields = [
        "article",
        "name",
        "description",
        "price",
        "unit",
        "stock_quantity",
        "discount",
        "photo",
        "category",
        "manufacturer",
        "supplier",
    ]
    success_url = reverse_lazy("product_list")

    def test_func(self):
        return is_admin(self.request.user)
