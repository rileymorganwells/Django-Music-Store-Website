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
        self.fields['pid'] = forms.CharField(label='id', widget=forms.HiddenInput())
        self.fields['quantity'] = forms.IntegerField(min_value=1, max_value=10)

    def clean(self):
        return self.cleaned_data

    def commit(self):
        #Grab product from database
        pid = self.cleaned_data.get('pid')
        qty = self.cleaned_data.get('quantity')
        product = cmod.Product.objects.all().filter(id=pid).first()
        #Grab cart. If there is no cart, create one
        self.order = cmod.Order.objects.all().filter(status='cart').first()
        if self.order is None:
            self.order = cmod.Order(status='cart', user=self.request.user)
        self.order.save()
        #Search for the product in the cart. If it's there already, just update it's quantity
        # if self.order.active_items().index(pid) is not None:
        #     item = self.order.get_item(pid)
        #     item.quantity += qty
        #     item.save()
        #Create order item, fill it with objects attributes
        self.orderItem = cmod.OrderItem()
        self.orderItem.product = product
        self.orderItem.price = product.price
        self.orderItem.quantity = qty
        self.orderItem.order = self.order
        self.orderItem.extended = qty * product.price
        self.orderItem.save() 
