from catalog import models as cmod

class LastFiveMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        pids = request.session.get('id')
        prods = []
        if request.session.get('id') is not None:
            for pid in pids:
                prods.append(cmod.Product.objects.get(id = pid))
        request.last_five = prods

        response = self.get_response(request)

        idlist = []
        for object in request.last_five:
            idlist.append(object.id)
        request.session['id'] = idlist

        return response
