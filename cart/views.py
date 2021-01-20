import os
from ftplib import FTP
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.views.generic.base import View
from cart.cart import Cart
from cart.forms import CartAddProductForm, CartCheckAllProductsForm
from website.models import Article, FavorisClient, ProfilUtilisateur
from order.models import HistoriqueCommande, ProduitCommande
from django.contrib import messages
import datetime
from datetime import date
from django.http import HttpResponseRedirect
import json
from django.conf import settings


class CartRemoveView(LoginRequiredMixin, View):
    """ Remove item """

    def get(self, request, **kwargs):
        context = {
            'id': kwargs['product_id'],
        }

        return render(request, 'cart/suppress_modal_mat.html', context)

    def post(self, request, **kwargs):
        cart = Cart(request)
        _pk = kwargs.get("product_id")
        product = get_object_or_404(Article, id=_pk)
        cart.remove(product)
        return redirect("cart:cart_detail")


class SendOrderView(LoginRequiredMixin, View):
    """ Send Order """

    @staticmethod
    def check_unity(self):
        if self is not None:
            return '{0:04}'.format(int(self))
        else:
            return '0000'

    @staticmethod
    def format_price(self):
        x = ' '
        rst = str(self).split('.')
        rst_join = rst[0] + rst[1]
        if len(rst_join) == 7:
            return self
        else:
            return (x * (6 - len(rst_join))) + str(self)

    @staticmethod
    def format_name(self):
        x = ' '
        if len(self) == 36:
            return self
        elif len(self) > 36:
            return self[0:37]
        else:
            return (x * (36 - len(self))) + self

    @staticmethod
    def format_quantity(self):
        x = ' '
        if len(self) == 10:
            return self
        else:
            return self + (x * (10 - len(self)))

    @staticmethod
    def send_file_to_ftp(self):
        try:
            ftp = FTP(settings.BERARD_FTP_HOST)
            ftp.set_debuglevel(2)
            ftp.login(settings.BERARD_FTP_USER, settings.BERARD_FTP_PWD)
            ftp.cwd('/Rep/IMPORT')
            file = open(self.name, 'rb')
            ftp.storbinary('STOR %s' % os.path.basename(self.name), file, 1024)
            file.close()

        except Exception as e:
            print('FTP ERROR ', e)
            raise e

    def get(self, request, **kwargs):
        return render(request, 'cart/confirm_modal_mat.html')

    def post(self, request, **kwargs):
        cart = Cart(request)
        if cart.get_total_price() < 200:
            messages.warning(request, 'Votre panier doit être de 200€ minimum')
            return redirect('cart:cart_detail')
        else:
            try:
                user = User.objects.get(id=request.user.id)
                order = HistoriqueCommande(
                    utilisateur=user
                )
                order.save()

                # to format hour with minute
                now = datetime.datetime.now()
                hour = '{:02d}'.format(now.hour)
                minute = '{:02d}'.format(now.minute)
                hour_with_minute = f'{hour}{minute}'

                # to format second with microsecond
                now = datetime.datetime.now()
                second = '{:02d}'.format(now.second)
                microsecond = str(now.microsecond // 1000)
                second_with_microsecond = f'{second}{microsecond}'

                # file to ftp
                file_name = '{}{}{}{}COMSOC.PLN'.format(
                    str(date.today()).replace('-', ''),
                    hour_with_minute,
                    second_with_microsecond,
                    f'_{user.profilutilisateur.code_representant}_')

                # if path not exists
                path = 'resources/export/'
                if not os.path.exists(path):
                    os.makedirs(path)

                # create file
                file = open(os.path.join(path, file_name), 'w')
                whitespace = ' '
                line1 = '!000C$01{code_client}00100{nom}#\n'
                line2 = '!000C$01{code_client}00104 Type facturation:N  Date livraison:         Date:  {date} Heure: {heure}                  #\n'
                context = {
                    "code_client": user.username,
                    "nom": user.last_name + whitespace * 64,
                    "date": str(date.today()).replace('-', ''),
                    "heure": hour_with_minute,
                }
                file.write(line1.format(**context))
                file.write(line2.format(**context))

                for item in cart:
                    article = Article.objects.get(id=item['article_id'])

                    # insert orders
                    item_order = ProduitCommande(
                        commande=order,
                        article=article,
                        prix=float(item['prix_achat']),
                        prix_HT=float(item['prix_ht']),
                        taux_TVA=float(item['tva']),
                        quantite=item['quantity'],
                    )
                    item_order.save()

                    # add favorites products for user
                    favorite, created = FavorisClient.objects.get_or_create(
                        utilisateur=request.user,
                        article=article,
                    )
                    favorite.quantite += item['quantity']
                    favorite.save()

                    # products line to ftp file
                    line3 = """!000C$01{code_client}0011{code_article}{prix_achat}{filler}{filler}PC{prix_achat}{filler}{libelle}{conditionnement}{quantite}{filler} #\n"""
                    context = {
                        "code_client": user.username,
                        "code_article": article.code_article + whitespace * 2,
                        "prix_achat": self.format_price(item['prix_achat']),
                        "libelle": self.format_name(article.libelle),
                        # "conditionnement": '{0:04}'.format(int(article.conditionnement)),
                        "conditionnement": self.check_unity(article.conditionnement),
                        "quantite": self.format_quantity('{:10.4f}'.format(item['quantity'])),
                        "filler": whitespace * 4
                    }
                    file.write(line3.format(**context))
                file.close()

                self.send_file_to_ftp(file)  # to send order to ftp server

                # cart.clear()
                cart.clear_all(cart)
                messages.success(request, 'Votre commande a bien été passée')

                return redirect("order:order_detail", pk=order.id)
            except:
                messages.error(request, "Votre commande n'a pas pu être éffectuée")
                return redirect("cart:cart_detail")


""" Cart actions """


@login_required(login_url="")
@require_POST
def order_summary_to_cart(request, order_id):
    order = HistoriqueCommande.objects.get(id=int(order_id))
    products = ProduitCommande.objects.filter(commande__id=int(order_id))
    cart = Cart(request)
    for item in products:
        product = get_object_or_404(Article, id=item.article.id)
        cart.add(product=product,
                 quantity=item.quantite,
                 )
    return redirect("cart:cart_detail")


@login_required(login_url="")
@require_POST
def cart_add(request, product_id):  # add method
    cart = Cart(request)
    product = get_object_or_404(Article, id=product_id)
    form = CartAddProductForm(request.POST)
    encoded_url = ''
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'])
        # redirect with hidden form
    encoded_url = cd['url'] or '/produit'
    return HttpResponseRedirect(encoded_url)


@login_required(login_url="")
def cart_detail(request):
    cart = Cart(request)
    quantity = CartCheckAllProductsForm
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
            initial={'quantity': item['quantity'],
                     'update': True})

    return render(request, 'cart/cart-detail.html', {'cart': cart, 'quantity': quantity})


@require_POST
def cart_update(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Article, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 update_quantity=True
                 )
    else:
        data = json.loads(request.body)
        cart.add(product=product,
                 quantity=int(data['quantity']),
                 update_quantity=True
                 )

    return redirect("cart:cart_detail")


@require_POST
def update_all_cart(request):
    cart = Cart(request)
    form = CartCheckAllProductsForm(request.POST)

    if form.is_valid():
        cd = form.cleaned_data
        try:
            tab_join = cd['quantity'].split(',')
            for i in tab_join:
                rst = i.split('/')
                try:
                    product = Article.objects.get(id=int(rst[0]))
                    if int(rst[1]) is not 0:
                        cart.add(product=product,
                                 quantity=int(rst[1]),
                                 update_quantity=True)
                except Article.DoesNotExist:
                    pass
        except ValueError:
            data = json.loads(request.body)
            for i in data['quantity']:
                rst = i.split('/')
                product = get_object_or_404(Article, id=int(rst[0]))
                cart.add(product=product,
                         quantity=int(rst[1]),
                         update_quantity=True)

    return redirect("cart:cart_detail")
