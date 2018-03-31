from django.conf import settings
from django_mako_plus import view_function, jscontext
from catalog import models as cmod
from catalog.models import Category
from django.http import HttpResponseRedirect
import math

@view_function
def process_request(request):
    cart = request.user.get_shopping_cart()
    tax = cmod.Product.objects.get(name="Tax")
    taxitem = cart.get_item(product=tax)
    cart.recalculate()
    context = {
        'cart': cart,
        'tax': taxitem,
    }
    return request.dmp.render('cart.html', context)

@view_function
def delete(request, orderItem:cmod.OrderItem):
    orderItem.status = 'deleted'
    orderItem.save()
    cart = request.user.get_shopping_cart()
    cart.recalculate()
    return HttpResponseRedirect('/catalog/cart/')