from django_mako_plus import view_function
from django import forms
from django.http import HttpResponseRedirect

@view_function
def process_request(request):
    if request.method == 'POST':
        form = TestForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/')
    else:
        form = TestForm()

    context = {
        'form': form,
    }
    return request.dmp_render('formtest.html', context)

class TestForm(forms.Form):
    comment = forms.CharField(label='Your comment')
    renewal_date = forms.DateField(help_text="Enter a date between now and 4 weeks (default 3)")
