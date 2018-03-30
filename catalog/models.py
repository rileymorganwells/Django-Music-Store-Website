from django.db import models
from polymorphic.models import PolymorphicModel
from django.conf import settings
import stripe
from decimal import *

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
        if self.images.all():
          url = settings.STATIC_URL + 'catalog/media/products/' + self.images.first().filename
        else:
          url = settings.STATIC_URL + 'catalog/media/products/image_unavailable.gif'
        return url

    def image_urls(self):
        if self.images.all(): #list of urls
          urls = []
          for image in self.images.all():
              urls.append(settings.STATIC_URL + 'catalog/media/products/' + image.filename)
        else:  #list of just unavailable
          urls = [settings.STATIC_URL + 'catalog/media/products/image_unavailable.gif']
        return urls

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

class Order(models.Model):
    '''An order in the system'''
    STATUS_CHOICES = (
        ( 'cart', 'Shopping Cart' ),
        ( 'payment', 'Payment Processing' ),
        ( 'sold', 'Finalized Sale' ),
    )
    order_date = models.DateTimeField(null=True, blank=True)
    name = models.TextField(blank=True, default="Shopping Cart")
    status = models.TextField(choices=STATUS_CHOICES, default='cart', db_index=True)
    total_price = models.DecimalField(max_digits=8, decimal_places=2, default=0) # max number is 999,999.99
    user = models.ForeignKey('account.User', related_name='orders',  on_delete=models.CASCADE)
    # shipping information
    ship_date = models.DateTimeField(null=True, blank=True)
    ship_tracking = models.TextField(null=True, blank=True)
    ship_name = models.TextField(null=True, blank=True)
    ship_address = models.TextField(null=True, blank=True)
    ship_city = models.TextField(null=True, blank=True)
    ship_state = models.TextField(null=True, blank=True)
    ship_zip_code = models.TextField(null=True, blank=True)

    def __str__(self):
        '''Prints for debugging purposes'''
        return 'Order {}: {}: {}'.format(self.id, self.user.get_full_name(), self.total_price)


    def active_items(self, include_tax_item=True):
        '''Returns the active items on this order'''
        # create a query object (filter to status='active')
        # if we aren't including the tax item, alter the query to exclude that OrderItem
        # I simply used the product name (not a great choice, but it is acceptable for credit)
        taxproduct = Product.objects.get(name="Tax")
        if include_tax_item:
            orderItems = OrderItem.objects.all().filter(status='active', order=self)
        else:
            orderItems = OrderItem.objects.all().filter(status='active', order=self).exclude(product=taxproduct)
        orderItemIDs = []
        if orderItems:
            for orderItem in orderItems:
                orderItemIDs.append(orderItem.product.id)
        return orderItemIDs

    def get_item(self, product, create=False):
        '''Returns the OrderItem object for the given product'''
        item = OrderItem.objects.filter(order=self, product=product, status='active').first()
        if item is None and create:
            item = OrderItem.objects.create(order=self, product=product, price=product.price, quantity=0)
        elif create and item.status != 'active':
            item.status = 'active'
            item.quantity = 0
        item.recalculate()
        item.save()
        return item


    def num_items(self):
        '''Returns the number of items in the cart'''
        items = 0
        for item in self.active_items():
            items += self.get_item(item).quantity
        return items
        #return sum(self.active_items(include_tax_item=False).values_list('quantity', flat=True))


    def recalculate(self):
        '''
        Recalculates the total price of the order,
        including recalculating the taxable amount.

        Saves this Order and all child OrderLine objects.
        '''
        # iterate the order items (not including tax item) and get the total price
        # call recalculate on each item
        taxproduct = Product.objects.get(name="Tax")
        total = 0
        for item in self.active_items(include_tax_item=False):
            orderItem = self.get_item(item)
            orderItem.recalculate()
            total += orderItem.extended
        # update/create the tax order item (calculate at 7% rate)
        tax = OrderItem.objects.get(product=taxproduct, order=self)
        tax.price = total * Decimal(.07)
        tax.price = round(tax.price,2)
        tax.save()
        total += tax.price
        # update the total and save
        self.total_price = total
        self.save()


    def finalize(self, stripe_charge_token):
        '''Runs the payment and finalizes the sale'''
        with transaction.atomic():
            # recalculate just to be sure everything is updated
            self.recalculate()
            # check that all products are available - try except!!!
            for item in self.active_items():
                if item.quantity > Product.objects.all().filter(product=item.product).quantity:
                    return 5
            # contact stripe and run the payment (using the stripe_charge_token)

            # finalize (or create) one or more payment objects
            payment = Payment.objects.create(order=self)
            # set order status to sold and save the order
            self.status = sold
            # update product quantities for BulkProducts
            # update status for IndividualProducts


class OrderItem(PolymorphicModel):
    '''A line item on an order'''
    STATUS_CHOICES = (
        ( 'active', 'Active' ),
        ( 'deleted', 'Deleted' ),
    )
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    status = models.TextField(choices=STATUS_CHOICES, default='active', db_index=True)
    product = models.ForeignKey(Product, null=True, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0) # max number is 999,999.99
    quantity = models.IntegerField(default=0)
    extended = models.DecimalField(max_digits=8, decimal_places=2, default=0) # max number is 999,999.99

    def __str__(self):
        '''Prints for debugging purposes'''
        return 'OrderItem {}: {}: {}'.format(self.id, self.product.name, self.extended)


    def recalculate(self):
        '''Updates the order item's price, quantity, extended'''
        # update the price if it isn't already set and we have a product
        if self.price is None:
            self.price = Product.objects.all().filter(product=self).price
        # default the quantity to 1 if we don't have a quantity set
        if self.quantity is None:
            self.quantity = 1
        # calculate the extended (price * quantity)
        extended = self.price * self.quantity
        # save the changes
        self.extended = extended
        self.save()


class Payment(models.Model):
    '''A payment on a sale'''
    order = models.ForeignKey(Order, null=True, on_delete=models.CASCADE)
    payment_date = models.DateTimeField(null=True, blank=True)
    amount = models.DecimalField(blank=True, null=True, max_digits=8, decimal_places=2) # max number is 999,999.99
    validation_code = models.TextField(null=True, blank=True)