from django.shortcuts import render
from django.views.generic import ListView

from .models import Product

def home(request):
    return render(request, 'mainapp/home.html')

class ProductListView(ListView):
    model = Product
    template_name = 'mainapp/product_list.html'
    context_object_name = 'products'
