from django.db import models

class Category():
    name = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    createdate = models.DateTimeField(blank=True, null=True)
    lastmodified = models.DateTimeField(blank=True, null=True)

# pip install django-polymorphic
class Product(PolymorphicModel):
        # polymorphic_ctype: 10
        # create_date: ! '2018-02-14 14:41:28.900082'
        # last_modified: ! '2018-02-14 14:41:28.900095'
        # status: A
        # name: Fight Song
        # description: By Rachel Platten and Dave Bassett
        # category: 1
        # price: '5.00'

class BulkProduct():
    name = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    category = models.TextField(blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    createdate = models.DateTimeField(blank=True, null=True)
    lastmodified = models.DateTimeField(blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    reordertrigger = models.IntegerField(blank=True, null=True)
    reorderquantity = models.IntegerField(blank=True, null=True)

class UniqueProduct():
    name = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    category = models.TextField(blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    createdate = models.DateTimeField(blank=True, null=True)
    lastmodified = models.DateTimeField(blank=True, null=True)
    itemID = models.IntegerField(blank=True, null=True)

class RentalProduct():
    name = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    category = models.TextField(blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    createdate = models.DateTimeField(blank=True, null=True)
    lastmodified = models.DateTimeField(blank=True, null=True)
    itemID = models.IntegerField(blank=True, null=True)
    # maxrental = models.
    retiredate = models.DateTimeField(blank=True, null=True)
    # def get_purchases(self):
    #     return [ 'Roku Ultimate 2000', 'USB Cable', 'Candy Bar' ]
