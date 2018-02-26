from django_mako_plus import view_function
from django import forms
from django.http import HttpResponseRedirect
from formlib.form import Formless

@view_function
def process_request(request):

    form = Contact(request)
    if form.is_valid():
        # once you get here, you cannet yell at the user anymore
        # this area is for an absolutely perfect form
        # ready to be processed
        # work of the form - create user, login user, purchase
        return HttpResponseRedirect('/')

    # render the form
    context = {
        'form': form,
    }
    return request.dmp.render('contact.html', context)

class Contact(Formless):

    def init(self):
        self.fields['name'] = forms.CharField(label='Name (first and last)')
        self.fields['email'] = forms.EmailField(label='Email')
        self.fields['comment'] = forms.CharField(label='Comment')
