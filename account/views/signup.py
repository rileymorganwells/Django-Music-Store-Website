from django_mako_plus import view_function
from django import forms
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from formlib.form import Formless
from account import models as amod
import re

@view_function
def process_request(request):

    form = TestForm(request)
    if form.is_valid():
        form.commit()
        return HttpResponseRedirect('/account/index/')

    # render the form
    context = {
        'form': form,
    }
    return request.dmp.render('signup.html', context)

class TestForm(Formless):

    def init(self):
        self.fields['first_name'] = forms.CharField(label='First Name')
        self.fields['last_name'] = forms.CharField(label='Last Name')
        self.fields['email'] = forms.EmailField(label='Email')
        self.fields['password'] = forms.CharField(max_length=32, widget=forms.PasswordInput, label='Password')
        self.fields['password2'] = forms.CharField(max_length=32, widget=forms.PasswordInput, label='Confirm Password')

    def clean_firstname(self):
        first_name = self.cleaned_data.get('first_name')
        return first_name

    def clean_lastname(self):
        last_name = self.cleaned_data.get('last_name')
        return last_name

    def clean_email(self):
        email = self.cleaned_data.get('email')
        e2 = amod.User.objects.filter(email=email)
        # check if this email already exists (objects.get thing)
        if len(e2) > 0:
            raise forms.ValidationError('This email already exists')
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if re.search('(?=.*\d).{8,}', password) is None:
            raise forms.ValidationError('Password must be at least 8 characters long and contain a number (0-9)')
        return password

    def clean(self):
        # for checking the entire form - usually two variables at once
        # "password" and "password2"
        if self.cleaned_data.get('password') != self.cleaned_data.get('password2'):
            raise forms.ValidationError('Passwords do not match!')
        return self.cleaned_data

    def commit(self):
        self.user = amod.User()
        self.user.first_name = self.cleaned_data.get('first_name')
        self.user.last_name = self.cleaned_data.get('last_name')
        self.user.email = self.cleaned_data.get('email')
        self.user.set_password(self.cleaned_data.get('password'))
        self.user.save()
        self.user = authenticate(email=self.cleaned_data.get('email'), password=self.cleaned_data.get('password'))
        login(self.request, self.user)
