from django.conf import settings
from django_mako_plus import view_function, jscontext
from datetime import datetime, timezone
from django.contrib.auth.decorators import login_required
from catalog import models as cmod

@view_function
@login_required
def process_request(request):
    orders = cmod.Order.objects.all().filter(user=request.user, status='sold')
    utc_time = datetime.utcnow()
    context = {
        # sent to index.html:
        'utc_time': utc_time,
        # sent to index.html and index.js:
        jscontext('utc_epoch'): utc_time.timestamp(),
        'orders': orders,
    }
    return request.dmp.render('index.html', context)
