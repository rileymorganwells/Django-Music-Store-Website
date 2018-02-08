from django_mako_plus import view_function
from django.http import HttpResponseRedirect
from django.contrib.auth import logout

@view_function
def process_request(request):
    #log the user account
    logout(request)
    return HttpResponseRedirect('/index/')
