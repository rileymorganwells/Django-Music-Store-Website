from django.conf import settings
from django_mako_plus import view_function, jscontext
from catalog import models as cmod
from catalog.models import Category

@view_function
def process_request(request, selection:cmod.Category):
    categories = cmod.Category.objects.all()
    context = {
        'category': categories,
        'selection': selection,
        'num_pages': 5,
    }
    return request.dmp.render('index.html', context)
