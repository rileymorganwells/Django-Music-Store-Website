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
        if request.user.is_authenticated:
            form.commit()
            cart = request.user.get_shopping_cart()
            cart.recalculate()
            return HttpResponseRedirect('/catalog/cart/')
        else:
            return HttpResponseRedirect('/account/signup/')

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

    def clean_quantity(self):
        prod = cmod.Product.objects.get(id=self.cleaned_data.get('pid'))
        try:
            qtyavail = prod.get_quantity() - cmod.OrderItem.objects.get(product=prod, status='active', order=self.request.user.get_shopping_cart()).quantity
        except:
            qtyavail = prod.get_quantity()
        quantity = self.cleaned_data.get('quantity')
        if quantity > qtyavail:
            if qtyavail == 0:
                raise forms.ValidationError('Sorry, ' + prod.name + ' is currently out of stock.')
            else:
                raise forms.ValidationError('Sorry, there are only ' + str(qtyavail) + ' products available!')
        return quantity

    def commit(self):
        #Grab product from database
        pid = self.cleaned_data.get('pid')
        qty = self.cleaned_data.get('quantity')
        product = cmod.Product.objects.get(id=pid)
        #Grab cart
        self.cart = self.request.user.get_shopping_cart()
        #Search for the product in the cart. If it's there already, just update it's quantity
        if product.id in self.cart.active_items():
            item = self.cart.get_item(pid)
            item.quantity += qty
            item.save()
        else:
        #Create order item, fill it with objects attributes
            self.orderItem = cmod.OrderItem()
            self.orderItem.product = product
            self.orderItem.price = product.price
            self.orderItem.quantity = qty
            self.orderItem.order = self.cart
            self.orderItem.extended = qty * product.price
            self.orderItem.save() 
