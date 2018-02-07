from django_mako_plus import view_function
from django import forms
from django.http import HttpResponseRedirect
from formlib.form import Formless

@view_function
def process_request(request):

    form = TestForm(request)
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
    return request.dmp_render('formtest.html', context)

class TestForm(Formless):

    def init(self):
        self.fields['email'] = forms.EmailField(label='Email')
        self.fields['Age'] = forms.IntegerField(label='Age', min_value=18)
        self.fields['renewal_date'] = forms.DateField(help_text="")
        self.fields['password'] = forms.CharField(max_length=32, widget=forms.PasswordInput, label='Password')
        self.fields['password2'] = forms.CharField(max_length=32, widget=forms.PasswordInput, label='Confirm Password')

    # def clean_email(self):
    #     un = self.cleaned_data.get('email')
    #
    #     # check if this email already exists (objects.get thing)
    #     if len(users) > 0:
    #         raise forms.ValidationError('Thie email already exists')
    #
    #     return un

    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age < 18:
            # show an error message: no soup for you
            raise forms.ValidationError('You are not 18, no soup for you')
        return age

    def clean(self):
        # for checking the entire form - usually two variables at once
        # "password" and "password2"
        pw1 = self.cleaned_data.get('password')
        pw2 = self.cleaned_data.get('password2')
        if pw1 != pw2:
            # yell at the user
            raise forms.ValidationError('Passwords do not match!')
        return self.cleaned_data
