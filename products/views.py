from django.shortcuts import render
from django.views.generic import ListView, DetailView

from products.mod_forms import ProductModelForm
from products.models import Product


def products(request, *args, **kwargs):
    if request.method == 'POST':
        form = ProductModelForm(request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
    else:
        form = ProductModelForm()
    context = {
        'items': Product.objects.all(),
        'form': form
    }
    return render(request, 'products/index.html', context=context)


class ProductsView(ListView):
    model = Product


class ProductDetail(DetailView):
    model = Product