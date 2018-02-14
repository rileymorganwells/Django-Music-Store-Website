from django.db import models

class Category():
    name = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    createdate = models.DateTimeField(blank=True, null=True)
    lastmodified = models.DateTimeField(blank=True, null=True)

# pip install django-polymorphic
# class Product(PolymorphicModel):
#         # polymorphic_ctype: 10
#         # create_date: ! '2018-02-14 14:41:28.900082'
#         # last_modified: ! '2018-02-14 14:41:28.900095'
#         # status: A
#         # name: Fight Song
#         # description: By Rachel Platten and Dave Bassett
#         # category: 1
#         # price: '5.00'

class BulkProduct():
    '''Bulk Product'''
    TITLE = 'Bulk'
    name = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    category = models.TextField(blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    createdate = models.DateTimeField(blank=True, null=True)
    lastmodified = models.DateTimeField(blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    reordertrigger = models.IntegerField(blank=True, null=True)
    reorderquantity = models.IntegerField(blank=True, null=True)
        # quantity: 20
        # reorder_trigger: 10
        # reorder_quantity: 10

class IndividualProduct():
    name = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    category = models.TextField(blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    createdate = models.DateTimeField(blank=True, null=True)
    lastmodified = models.DateTimeField(blank=True, null=True)
    itemID = models.IntegerField(blank=True, null=True)
        # pid: 12345X6

class RentalProduct():
    name = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    category = models.TextField(blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    createdate = models.DateTimeField(blank=True, null=True)
    lastmodified = models.DateTimeField(blank=True, null=True)
    itemID = models.IntegerField(blank=True, null=True)
    retiredate = models.DateTimeField(blank=True, null=True)
        # pid: MACK12A
        # max_rental_days: 2
        # retire_date: null
