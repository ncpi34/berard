from django import template
from website.models import Article

register = template.Library()

@register.filter
def without_taxes(tarif, article):
    tarif = tarif or "0"
    price = article.get_price_without_taxes(tarif)
    return price