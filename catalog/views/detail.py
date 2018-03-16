from django.conf import settings
from django_mako_plus import view_function, jscontext
from catalog import models as cmod
import math

@view_function
def process_request(request, product:cmod.Product=None):
    products = cmod.Product.objects.all()
    if product in request.last_five:
        request.last_five.remove(product)
    request.last_five.insert(0, product)
    if len(request.last_five) > 6:
        del request.last_five[-1]

    context = {
        'product': product,
    }
    return request.dmp.render('detail.html', context)
