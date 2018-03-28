from django.conf import settings
from django_mako_plus import view_function, jscontext
from catalog import models as cmod
from django import forms
from formlib.form import Formless
from django.http import HttpResponseRedirect
import math

@view_function
def process_request(request, product:cmod.Product=None):
    prodict = product.__dict__
    prodict['pid'] = product.id
    productclass = product.__class__.__name__
    if productclass == 'BulkProduct':
        prodict['max'] = product.quantity
    else:
        prodict['quantity'] = 1
    products = cmod.Product.objects.all()
    if product in request.last_five:
        request.last_five.remove(product)
    request.last_five.insert(0, product)
    if len(request.last_five) > 6:
        del request.last_five[-1]

    form = AddToCart(request, initial=prodict)
    form.submit_text = form.buy_now_text
    if form.is_valid():
        form.commit()
        return HttpResponseRedirect('/catalog/cart/')

    context = {
        'product': product,
        'form': form,
    }
    return request.dmp.render('detail.html', context)

class AddToCart(Formless):

    def init(self):
        self.fields['pid'] = forms.CharField(label='id')
        self.fields['quantity'] = forms.IntegerField(min_value=1, max_value=10)

    def clean(self):
        return self.cleaned_data

    def commit(self):
        pid = self.cleaned_data.get('pid')
        self.order = cmod.Order.objects.all().filter(status='cart').first()
        if self.order is None:
            self.order = cmod.Order(status='cart')
        self.order.save()
        self.orderItem = cmod.OrderItem()
        self.orderItem.quantity = self.cleaned_data.get('quantity')
        self.orderItem.order = self.order
        self.orderItem.product = cmod.Product.objects.all().filter(id=pid).first()
        self.orderItem.save() 
