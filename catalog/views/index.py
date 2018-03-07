from django.conf import settings
from django_mako_plus import view_function, jscontext
from catalog import models as cmod
from catalog.models import Category
import math

@view_function
def process_request(request, selection:cmod.Category=None):
    categories = cmod.Category.objects.all().order_by('name')
    products = cmod.Product.objects.all()
    if selection is not None:
        products = products.filter(category=selection)
        cid = selection.id
    else:
        cid = 0
    context = {
        'category': categories,
        'selection': selection,
        'num_pages': math.ceil(products.count()/6),
        jscontext('cid'): cid,
        jscontext('pnum'): math.ceil(products.count()/6),
    }
    return request.dmp.render('index.html', context)

@view_function
def products(request, selection:cmod.Category=None, pnum:int=1):
    #do work
    products = cmod.Product.objects.all().order_by('name')
    if selection is not None:
        products = products.filter(category=selection).order_by('name')
    products = products[(pnum-1)*6:pnum*6]
    context = {
        'products': products,
        'pnum': pnum,
    }
    return request.dmp.render('index.products.html', context)
