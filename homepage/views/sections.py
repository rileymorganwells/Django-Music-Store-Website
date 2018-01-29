from django.conf import settings
from django_mako_plus import view_function, jscontext
from datetime import datetime, timezone

@view_function
def process_request(request):
    utc_year = datetime.utcnow().year
    context = {
        # sent to index.html:
        'utc_year': utc_year,
    }
    return request.dmp_render('sections.html', context)
