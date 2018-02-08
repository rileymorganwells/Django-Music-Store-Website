from django_mako_plus import view_function
from django import forms
from django.http import HttpResponseRedirect
from formlib.form import Formless
from django.core.validators import RegexValidator

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
    return request.dmp_render('signup.html', context)

class TestForm(Formless):

    def init(self):
        self.fields['email'] = forms.EmailField(label='Email')
        self.fields['password'] = forms.CharField(max_length=32, widget=forms.PasswordInput, label='Password', validators=[
            RegexValidator(
                regex=r'\d',
                message='Password must contain a number (0-9)')])
        self.fields['password2'] = forms.CharField(max_length=32, widget=forms.PasswordInput, label='Confirm Password')

    # def clean_email(self):
    #     un = self.cleaned_data.get('email')
    #
    #     # check if this email already exists (objects.get thing)
    #     if len(users) > 0:
    #         raise forms.ValidationError('Thie email already exists')
    #
    #     return un

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise forms.ValidationError('Password must be at least 8 characters long')
        # if RegexValidator('\d', password) is not None: #NEED TO GET RE IN HERE SOMEHOW
        #     raise forms.ValidationError('Password must contain a number (0-9)')
        return password

    def clean(self):
        # for checking the entire form - usually two variables at once
        # "password" and "password2"
        if self.cleaned_data.get('password') != self.cleaned_data.get('password2'):
            # yell at the user
            raise forms.ValidationError('Passwords do not match!')
        return self.cleaned_data
