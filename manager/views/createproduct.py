from django.conf import settings
from django_mako_plus import view_function, jscontext
from catalog import models as cmod

@view_function
def process_request(request):
    products = cmod.Product.objects.all()
    context = {
        'name': products,
    }
    return request.dmp_render('createproduct.html', context)
