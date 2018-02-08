from django_mako_plus import view_function
from django.http import HttpResponseRedirect

@view_function
def process_request(request):
    #log the user account

    return HttpResponseRedirect('/index/')
