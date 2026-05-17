from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView

from .models import Product, Cart, CartItem


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
    """Доступна только пользователям с ролью admin."""

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

class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Редактирование товара. Доступна только для роли admin."""

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

@login_required
@user_passes_test(is_admin)
def product_delete_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        product.delete()
        return redirect("product_list")
    return render(request, "mainapp/product_confirm_delete.html", {"product": product})

@login_required
@user_passes_test(is_admin)
def product_cancel_edit(request, pk):
    return redirect("product_list")


from .models import Cart, CartItem


@login_required
def cart_view(request):
    """Страница корзины текущего пользователя."""
    cart, _ = Cart.objects.get_or_create(user=request.user)
    return render(request, "mainapp/cart.html", {"cart": cart})


@login_required
def cart_add(request, pk):
    """Добавить товар в корзину или увеличить количество."""
    product = get_object_or_404(Product, pk=pk)
    cart, _ = Cart.objects.get_or_create(user=request.user)
    item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        item.quantity += 1
        item.save()
    return redirect("cart")


@login_required
def cart_remove(request, pk):
    """Удалить позицию из корзины."""
    cart = get_object_or_404(Cart, user=request.user)
    item = get_object_or_404(CartItem, cart=cart, pk=pk)
    if request.method == "POST":
        item.delete()
    return redirect("cart")
