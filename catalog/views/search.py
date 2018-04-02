from django.conf import settings
from django_mako_plus import view_function
from django.contrib.auth.decorators import permission_required
from catalog import models as cmod
from django.http import JsonResponse

@permission_required('') ### WHAT DO I PUT IN HERE???
@view_function
def process_request(request, category=None, product=None, max_price=None, page=None):
    # create json dictionary
    json = {}
    json['Products'] = []
    # grab products
    products = cmod.Product.objects.all().order_by('category','name')
    if category:
        cat = cmod.Category.objects.get(name__icontains=category)
        products = products.filter(category=cat)
    if product:
        products = products.filter(name__icontains=product)
    if max_price:
        products = products.filter(price__lte=max_price)
    if page:
        last = (int(page)*6)
        first = last - 6
        products = products[first:last]
    # add each product to list
    for p in products:
        prod = {
            'category':p.category.name,
            'name':p.name,
            'price':p.price
        }
        json['Products'].append(prod)
    # return json
    return JsonResponse(json)
