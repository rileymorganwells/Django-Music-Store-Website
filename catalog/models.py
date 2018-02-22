from django.db import models
from polymorphic.models import PolymorphicModel

class Category(models.Model):
    name = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    create_date = models.DateTimeField(blank=True, null=True)
    last_modified = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name

# pip install django-polymorphic
class Product(PolymorphicModel):
    '''Bulk, individual, or rental product'''
    TYPE_CHOICES = (
        ('BulkProduct', 'Bulk Product'),
        ('IndividualProduct', 'Individual Product'),
        ('RentalProduct', 'Rental Product'),
    )
    STATUS_CHOICES = (
        ('A', 'Active'),
        ('I', 'Inactive'),
    )
    create_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    status = models.TextField(choices=STATUS_CHOICES, default='A')
    name = models.TextField()
    description = models.TextField()
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=7, decimal_places=2)

    def get_quantity(self):
        return self.quantity

class BulkProduct(Product):
    '''Bulk Product'''
    TITLE = 'Bulk'
    quantity = models.IntegerField()
    reorder_trigger = models.IntegerField()
    reorder_quantity = models.IntegerField()

    def get_quantity(self):
        return self.quantity

class IndividualProduct(Product):
    '''A product tracked individually'''
    TITLE = 'Individual'
    pid = models.TextField()

    def get_quantity(self):
        return 1

class RentalProduct(Product):
    '''Products to be rented'''
    TITLE = 'Rental'
    pid = models.TextField()
    max_rental_days = models.IntegerField(default=0)
    retire_date = models.DateTimeField(null=True, blank=True)

    def get_quantity(self):
        return 1
