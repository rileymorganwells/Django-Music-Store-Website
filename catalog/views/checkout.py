from django.conf import settings
from django_mako_plus import view_function, jscontext
from catalog import models as cmod
from django import forms
from formlib.form import Formless
from django.http import HttpResponseRedirect
import sys, traceback
import math

@view_function
def process_request(request):
    cart = cmod.Order.objects.get(user=request.user)
    cart.recalculate()
    form = Checkout(request)
    form.submit_text = form.checkout_text
    if form.is_valid():
        form.commit()
        return HttpResponseRedirect('/catalog/thankyou/')

    context = {
        'cart': cart,
        'form': form,
    }
    return request.dmp.render('checkout.html', context)

class Checkout(Formless):

    def init(self):
        self.fields['stripeToken'] = forms.CharField(widget=forms.HiddenInput())
        self.fields['street1'] = forms.CharField(label='Street Address 1')
        self.fields['street2'] = forms.CharField(label='Street Address 2')
        self.fields['city'] = forms.CharField(label='City')
        self.fields['state'] = forms.CharField(label='State')
        self.fields['zip'] = forms.CharField(label='Zip Code')

    def clean(self):
        cart = self.request.user.get_shopping_cart()
        try:
            cart.finalize(self.cleaned_data.get('stripeToken'))
        except:
            traceback.print_exc()
            raise forms.ValidationError('There was an error with your payment information. Please try again.')
        return self.cleaned_data

    def commit(self):
        return 5