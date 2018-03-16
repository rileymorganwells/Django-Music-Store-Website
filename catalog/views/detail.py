from django.conf import settings
from django_mako_plus import view_function, jscontext
from catalog import models as cmod
import math

@view_function
def process_request(request, product:cmod.Product=None):
    products = cmod.Product.objects.all()
    context = {
        'product': product,
    }
    return request.dmp.render('detail.html', context)
