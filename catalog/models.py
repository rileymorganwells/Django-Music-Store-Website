from django.db import models
from polymorphic.models import PolymorphicModel
from django.conf import settings

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
        ('1', 'Individual Product'),
        ('2', 'Bulk Product'),
        ('3', 'Rental Product'),
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

    def image_url(self):
        '''Returns the first image on this product as a image_url
            OR if no images, the "unavailable" image url.
        '''
        # always returns a url
        if len(self.images.all()) > 0:
          url = settings.STATIC_URL + '/catalog/media/products/' + self.images.all()[0].filename
        else:
          url = settings.STATIC_URL + 'catalog/media/products/image_unavailable.gif'
        return url

    def image_urls(self):
        if self.images.all() > 0: #list of urls
          url = settings.STATIC_URL + '/catalog/media/products/' + self.images.all()[0].filename
        else:  #list of just unavailable
          url = default (image_unavailable.gif)
        return url

class ProductImage(models.Model):
    filename = models.TextField()
    product = models.ForeignKey(Product, related_name="images", on_delete=models.CASCADE)

class IndividualProduct(Product):
    '''A product tracked individually'''
    TITLE = 'Individual Product'
    pid = models.TextField()

    def get_quantity(self):
        return 1

class BulkProduct(Product):
    '''Bulk Product'''
    TITLE = 'Bulk Product'
    quantity = models.IntegerField()
    reorder_trigger = models.IntegerField()
    reorder_quantity = models.IntegerField()

    def get_quantity(self):
        return self.quantity

class RentalProduct(Product):
    '''Products to be rented'''
    TITLE = 'Rental Product'
    pid = models.TextField()
    max_rental_days = models.IntegerField(null=True, default=0)
    retire_date = models.DateTimeField(null=True, blank=True)

    def get_quantity(self):
        return 1

# class ProductImage(models.Model):
#     product = models.ForeignKey(Product, related_name="images")
