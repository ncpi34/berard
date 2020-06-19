from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import DeleteView
from django.views.generic.base import View

from cart.cart import Cart
from cart.forms import CartAddProductForm
from website.models import Article, HistoriqueCommande, ProduitCommande
from django.contrib import messages

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


# @login_required(login_url="")
# def cart_remove(request, product_id):
#     cart = Cart(request)
#     product = get_object_or_404(Article, id=product_id)
#     cart.remove(product)
#     return redirect("cart:cart_detail")

# Remove item from cart with modal
class CartRemoveView(LoginRequiredMixin, View):

    def get(self, request, **kwargs):
        return render(request, 'cart/delete_item.html')

    def post(self, request, **kwargs):
        cart = Cart(request)
        _pk = kwargs.get("product_id")
        product = get_object_or_404(Article, id=_pk)
        cart.remove(product)
        return redirect("cart:cart_detail")


# Confirm Cart orders
class SendOrderView(LoginRequiredMixin, View):

    def get(self, request, **kwargs):
        return render(request, 'cart/confirm_cart.html')

    def post(self, request, **kwargs):
        try:
            cart = Cart(request)

            user_id = User.objects.get(id=request.user.id)
            order = HistoriqueCommande(
                utilisateur=user_id
            )
            order.save()

            for item in cart:
                article_id = Article.objects.get(id=item['article_id'])
                item_order = ProduitCommande(
                    commande=order,
                    article=article_id,
                    prix=float(item['prix_achat']),
                    quantite=item['quantity'],
                )
                item_order.save()
            # cart.clear()
            cart.clear_all(cart)
            messages.success(request, 'Votre commande a bien été passée')
            return redirect("cart:cart_detail")
            # return redirect("website:products")
        except Exception as e:
            print("ERROR champs ", e)
            messages.error(request, "Votre commande n'a pas être éffectuée")
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
