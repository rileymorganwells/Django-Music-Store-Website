from django.db import models
from cuser.models import AbstractCUser
from catalog import models as cmod

class User(AbstractCUser):
    birthdate = models.DateField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.TextField(blank=True, null=True)
    state = models.TextField(blank=True, null=True)
    zip = models.TextField(blank=True, null=True)

    def get_purchases(self):
        return [ 'Roku Ultimate 2000', 'USB Cable', 'Candy Bar' ]

    def get_shopping_cart(self):
        try:
            cart = cmod.Order.objects.get(status='cart', user=self)
        except:
            cart = cmod.Order(status='cart', user=self)
            cart.save()
        return cart
