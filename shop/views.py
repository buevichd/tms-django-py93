from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, Http404
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Order, OrderEntry


def products_view(request):
    context = {'products': Product.objects.all()}
    return render(request, 'shop/products.html', context)


def product_detail(request, product_id: int):
    context = {'product': get_object_or_404(Product, id=product_id)}
    return render(request, 'shop/product_detail.html', context)


@login_required
def add_to_cart(request: HttpRequest, product_id: int):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        request.user.profile.shopping_cart.add_product(product)
    return redirect('shop:product_detail', product_id)


