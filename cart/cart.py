from decimal import Decimal
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect
from website.models import Article

"""Cart Module"""


class Cart(object):

    def __init__(self, request):
        """
        Initialization
        """
        self.request = request
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):
        """
        Iterate over the items in the cart and get products from DB
        """
        products_ids = self.cart.keys()
        # get the product obj and add them to the cart
        products = Article.objects.filter(id__in=products_ids)

        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['prix_achat'] = Decimal(item['prix_achat'])
            item['total_price'] = item['prix_achat'] * item['quantity']
            yield item

    def __len__(self):
        """
        Count all items in the cart
        """
        return sum(item['quantity'] for item in self.cart.values())

    def add(self, product, quantity=1, update_quantity=False):
        """
        Add a product to the cart or update its quantity.
        """
        id = str(product.id)
        # newItem = True
        if product.id not in self.cart.keys() and quantity is not 0:
            self.cart[product.id] = {
                'userid': self.request.user.id,
                'article_id': id,
                'libelle': product.libelle,
                'quantity': 0,
                'prix_achat': str(self.get_price_by_user(product)),
                'image': product.image,
                'code_article': product.code_article,
            }
            if update_quantity and quantity is not 0:
                self.cart[product.id]['quantity'] = quantity
            else:
                self.cart[product.id]['quantity'] += quantity
            self.save()

    def save(self):
        # update the session cart
        self.session[settings.CART_SESSION_ID] = self.cart
        # mark the session as "modified" to make sure it is saved
        self.session.modified = True

    def get_price_by_user(self, product):
        tarif_id = self.request.session.get('tarif')
        # return product[tarif]
        if tarif_id == 1:
            return product.prix_achat_1
        elif tarif_id == 2:
            return product.prix_achat_2
        elif tarif_id == 3:
            return product.prix_achat_3
        else:
            return product.prix_achat_4

    def remove(self, product):
        """
        Remove a product from the cart.
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def get_total_price(self):
        """
        Get price of the cart
        """
        return sum(Decimal(item['prix_achat']) * item['quantity'] for item in self.cart.values())

    def clear(self):  # remove cart from session
        try:
            del self.cart
            self.save()
        except Exception as e:
            print('CART ERROR', e)

    def clear_all(self, products):  # remove all item in cart
        try:
            for product in products:
                product_id = str(product['article_id'])
                if product_id in self.cart:
                    del self.cart[product_id]
                    self.save()
        except Exception as e:
            print('ERRORR CLEANNING CART', e)

    def decrement(self, product):
        for key, value in self.cart.items():
            if key == str(product.id):
                value['quantité'] = value['quantité'] - 1
                if value['quantité'] < 1:
                    return redirect('cart:cart_detail')
                self.save()
                break
            else:
                print("Erreur panier")
