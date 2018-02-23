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
        self.fields['type'] = forms.ChoiceField(label='Product Type', choices=[ ['1', 'Individual'], ['2', 'Bulk'], ['3', 'Rental']])
        self.fields['name'] = forms.CharField(label='Product Name')
        self.fields['description'] = forms.CharField(label='Product Description')
        self.fields['category'] = forms.ModelChoiceField(queryset=cmod.Category.objects.all(), label='Category')
        self.fields['price'] = forms.DecimalField(label='Price')
        self.fields['quantity'] = forms.IntegerField(label='Quantity', required=False)
        self.fields['reorder_trigger'] = forms.CharField(max_length=32, label='Reorder Trigger', required=False)
        self.fields['reorder_quantity'] = forms.CharField(max_length=32, label='Reorder Quantity', required=False)
        self.fields['pid'] = forms.CharField(label='pid', required=False)
        self.fields['max_rental_days'] = forms.IntegerField(label='Max Rental Days', required=False)
        self.fields['retire_date'] = forms.DateTimeField(label='Retire Date', required=False)
        self.fields['create_date'] = forms.DateTimeField(label='Create Date')
        self.fields['last_modified'] = forms.DateTimeField(label='Last Modified')

    def clean_type(self):
        type = self.cleaned_data.get('type')
        return type

    def clean_type(self):
        name = self.cleaned_data.get('name')
        return name

    def clean_type(self):
        description = self.cleaned_data.get('description')
        return description

    def clean_type(self):
        category = self.cleaned_data.get('category')
        return category

    def clean_type(self):
        price = self.cleaned_data.get('price')
        return price

    def clean_type(self):
        quantity = self.cleaned_data.get('quantity')
        return quantity

    def clean_type(self):
        reorder_trigger = self.cleaned_data.get('reorder_trigger')
        return reorder_trigger

    def clean_type(self):
        reorder_quantity = self.cleaned_data.get('reorder_quantity')
        return reorder_quantity

    def clean_type(self):
        pid = self.cleaned_data.get('pid')
        return pid

    def clean_type(self):
        max_rental_days = self.cleaned_data.get('max_rental_days')
        return max_rental_days

    def clean_type(self):
        retire_date = self.cleaned_data.get('retire_date')
        return retire_date

    def clean_type(self):
        create_date = self.cleaned_data.get('create_date')
        return create_date

    def clean_type(self):
        last_modified = self.cleaned_data.get('last_modified')
        return last_modified

    def commit(self):
        if self.cleaned_data.get('type') == 1:
            self.product = cmod.IndividualProduct()
            self.product.pid = self.cleaned_data.get('pid')
        elif self.cleaned_data.get('type') == 2:
            self.product = cmod.BulkProduct()
            self.product.quantity = self.cleaned_data.get('quantity')
            self.product.reorder_trigger = self.cleaned_data.get('reorder_trigger')
            self.product.reorder_quantity = self.cleaned_data.get('reorder_quantity')
        else:
            self.product = cmod.RentalProduct()
            self.product.pid = self.cleaned_data.get('pid')
            self.product.max_rental_days = self.cleaned_data.get('max_rental_days')
            self.product.retiredate = self.cleaned_data.get('retiredate')
        self.product.name = self.cleaned_data.get('name')
        self.product.description = self.cleaned_data.get('description')
        self.product.category = self.cleaned_data.get('category')
        self.product.price = self.cleaned_data.get('price')
        self.product.create_date = self.cleaned_data.get('create_date')
        self.product.last_modified = self.cleaned_data.get('last_modified')
        self.product.save()

@view_function
def edit(request, product:cmod.Product):
    prodict = product.__dict__
    form = EditProduct(request, prodict)
    if form.is_valid():
        form.commit()
        return HttpResponseRedirect('/manager/products/')

    # render the form
    context = {
        'form': form,
        'product': product,
    }
    return request.dmp_render('edit.html', context)

class EditProduct(Formless):

    def init(self):
        self.fields['type'] = forms.ChoiceField(label='Product Type', choices=[ ['1', 'Individual'], ['2', 'Bulk'], ['3', 'Rental']])
        self.fields['name'] = forms.CharField(label='Product Name')
        self.fields['description'] = forms.CharField(label='Product Description')
        self.fields['category'] = forms.ModelChoiceField(queryset=cmod.Category.objects.all(), label='Category')
        self.fields['price'] = forms.CharField(max_length=32, label='Price')
        self.fields['quantity'] = forms.CharField(max_length=32, label='Quantity', required=False)
        self.fields['reorder_trigger'] = forms.CharField(max_length=32, label='Reorder Trigger', required=False)
        self.fields['reorder_quantity'] = forms.CharField(max_length=32, label='Reorder Quantity', required=False)
        self.fields['pid'] = forms.CharField(label='pid', required=False)
        self.fields['max_rental_days'] = forms.IntegerField(label='Max Rental Days', required=False)
        self.fields['retire_date'] = forms.DateTimeField(label='Retire Date', required=False)
        self.fields['create_date'] = forms.DateTimeField(label='Create Date')
        self.fields['last_modified'] = forms.DateTimeField(label='Last Modified')

    def commit(self):
        self.product = cmod.Product.objects.get(id=50)
        self.product.name = "test"
        self.product.save()

@view_function
def delete(request, product:cmod.Product):
    product.status = 'I'
    product.save()
    return HttpResponseRedirect('/manager/products/')
