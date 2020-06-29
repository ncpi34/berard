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
import datetime
from datetime import date

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

            user = User.objects.get(id=request.user.id)
            order = HistoriqueCommande(
                utilisateur=user
            )
            order.save()

            # to format hour with minute
            now = datetime.datetime.now()
            hour = '{:02d}'.format(now.hour)
            minute = '{:02d}'.format(now.minute)
            hour_with_minute = '{}{}'.format(hour, minute)

            # file to ftp
            file = open('test.PLN', 'w')
            line1 = '!000C$01{code_client}00100{nom}                                                            #\n'
            line2 = '!000C$01{code_client}00104    Type  facturation:N   Date    livraison:      Date:  {date}  Heure:  {heure}   #\n'
            context = {
                "code_client": user.username,
                "nom": user.last_name,
                "date": str(date.today()).replace('-', ''),
                "heure": hour_with_minute,
            }
            file.write(line1.format(**context))
            file.write(line2.format(**context))

            for item in cart:
                article = Article.objects.get(id=item['article_id'])

                item_order = ProduitCommande(
                    commande=order,
                    article=article,
                    prix=float(item['prix_achat']),
                    quantite=item['quantity'],
                )
                item_order.save()

                # products line to ftp file
                line3 = """!000C$01{code_client}001{code_article}   {prix_achat}    PC  {prix_achat}   {libelle}   {conditionnement}   {quantite} #\n"""
                context = {
                    "code_client": user.username,
                    "code_article": article.code_article,
                    "prix_achat": item['prix_achat'],
                    "libelle": article.libelle,
                    "conditionnement": '{0:04}'.format(int(article.conditionnement)),
                    "quantite": '{:10.4f}'.format(item['quantity']),
                }
                file.write(line3.format(**context))
            file.close()

            # cart.clear()
            cart.clear_all(cart)
            messages.success(request, 'Votre commande a bien été passée')
            return redirect("cart:cart_detail")
            # return redirect("website:products")
        except Exception as e:
            print("ERROR champs ", e)
            messages.error(request, "Votre commande n'a pas pu être éffectuée")
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
