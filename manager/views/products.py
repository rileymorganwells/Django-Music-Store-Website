from django.conf import settings
from django_mako_plus import view_function, jscontext
from catalog import models as cmod
from catalog.models import Product

@view_function
def process_request(request):
    products = cmod.Product.objects.filter(status='A')
    context = {
        'name': products,
    }
    return request.dmp.render('products.html', context)
