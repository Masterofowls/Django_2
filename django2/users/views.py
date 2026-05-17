from django.contrib.auth import login
from django.shortcuts import redirect, render

from .forms import RegisterForm


def register_view(request):
    """Регистрация нового пользователя с ролью client."""
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = RegisterForm()
    return render(request, "users/register.html", {"form": form})
