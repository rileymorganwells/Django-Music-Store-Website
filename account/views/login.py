from django_mako_plus import view_function
from django import forms
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from formlib.form import Formless

@view_function
def process_request(request):

    form = MyForm(request)
    if form.is_valid():
        form.commit()
        return HttpResponseRedirect('/account/index/')

    return request.dmp.render('login.html', {
        'form': form,
    })

class MyForm(Formless):

    def init(self):
        self.fields['email'] = forms.CharField(label='Email Address')
        self.fields['password'] = forms.CharField(max_length=32, widget=forms.PasswordInput, label='Password')
        # self.user = None

    def clean(self):
        self.user = authenticate(email=self.cleaned_data.get('email'), password=self.cleaned_data.get('password'))
        if self.user is None:
            raise forms.ValidationError('Invalid email or password.')
        # login(self.request, self.user)
        return self.cleaned_data

    def commit(self):
        login(self.request, self.user)
