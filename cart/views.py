from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.views.decorators.http import require_POST

from cart.cart import Cart
from cart.forms import CartAddProductForm
from website.models import Article

""" Cart """


@login_required(login_url="")
@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Article, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'])
    # return redirect("cart:cart_detail")
    return redirect("website:products")


@login_required(login_url="")
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Article, id=product_id)
    cart.remove(product)
    return redirect("cart:cart_detail")


@login_required(login_url="")
def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
            initial={'quantity': item['quantity'],
                     'update': True})
    return render(request, 'cart/cart-detail.html', {'cart': cart})


# modify quantity from cart
@require_POST
def cart_update(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Article, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'])
    # return redirect("cart:cart_detail")
    return redirect("cart:cart_detail")
