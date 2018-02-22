from django.conf import settings
from django_mako_plus import view_function, jscontext
from catalog import models as cmod
from formlib.form import Formless
from django.http import HttpResponseRedirect
from django import forms

@view_function
def create(request):

    form = CreateProduct(request)
    if form.is_valid():
        form.commit()
        return HttpResponseRedirect('/manager/products/')

    # render the form
    context = {
        'form': form,
    }
    return request.dmp_render('create.html', context)

class CreateProduct(Formless):

    def init(self):
        self.fields['name'] = forms.CharField(label='Product Name')
        self.fields['description'] = forms.CharField(label='Product Description')
        self.fields['category'] = forms.ModelChoiceField(queryset=cmod.Category.objects.all(), label='Category')
        self.fields['type'] = forms.ChoiceField(label='Type')
        self.fields['price'] = forms.CharField(max_length=32, widget=forms.PasswordInput, label='Price')
        self.fields['quantity'] = forms.CharField(max_length=32, widget=forms.PasswordInput, label='Quantity')
        self.fields['reorder_trigger'] = forms.CharField(max_length=32, widget=forms.PasswordInput, label='Reorder Trigger')
        self.fields['reorder_quantity'] = forms.CharField(max_length=32, widget=forms.PasswordInput, label='Reorder Quantity')
        self.fields['pid'] = forms.CharField(label='pid')
        self.fields['max_rental_days'] = forms.IntegerField(label='Max Rental Days')
        self.fields['retire_date'] = forms.DateTimeField(label='Retire Date')
        self.fields['create_date'] = forms.DateTimeField(label='Create Date')
        self.fields['last_modified'] = forms.DateTimeField(label='Last Modified')

    def commit(self):
        self.product = cmod.Product()
        self.product.name = "test"
        self.user.save()

@view_function
def edit(request, product:cmod.Product):

    form = EditProduct(request)
    if form.is_valid():
        form.commit()
        return HttpResponseRedirect('/manager/products/')

    # render the form
    context = {
        'form': form,
        'product': product
    }
    return request.dmp_render('edit.html', context)

class EditProduct(Formless):

    def init(self):
        self.fields['name'] = forms.CharField(label='Product Name')
        self.fields['description'] = forms.CharField(label='Product Description')
        self.fields['category'] = forms.ModelChoiceField(queryset=cmod.Category.objects.all(), label='Category')
        self.fields['type'] = forms.ChoiceField(label='Type')
        self.fields['price'] = forms.CharField(max_length=32, widget=forms.PasswordInput, label='Price')
        self.fields['quantity'] = forms.CharField(max_length=32, widget=forms.PasswordInput, label='Quantity')
        self.fields['reorder_trigger'] = forms.CharField(max_length=32, widget=forms.PasswordInput, label='Reorder Trigger')
        self.fields['reorder_quantity'] = forms.CharField(max_length=32, widget=forms.PasswordInput, label='Reorder Quantity')
        self.fields['pid'] = forms.CharField(label='pid')
        self.fields['max_rental_days'] = forms.IntegerField(label='Max Rental Days')
        self.fields['retire_date'] = forms.DateTimeField(label='Retire Date')
        self.fields['create_date'] = forms.DateTimeField(label='Create Date')
        self.fields['last_modified'] = forms.DateTimeField(label='Last Modified')

    def commit(self):
        self.product = cmod.Product()
        self.product.name = "test"
        self.product.save()

@view_function
def delete(request, product:cmod.Product):
    return request.dmp_render('products.edit.html', product)
