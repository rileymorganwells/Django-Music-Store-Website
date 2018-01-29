from django.conf import settings
from django_mako_plus import view_function

@view_function
def process_request(request):

    if request.method == 'POST':
        print(request.POST['fname'])
        print(request.POST['lname'])

    context = {
    }
    return request.dmp_render('contact.html', context)
