# All apps that are DMP-enabled must have this setting in their app-level __init__.py
DJANGO_MAKO_PLUS = True

# from django.http import Http404
# from django_mako_plus import set_default_converter, DefaultConverter
# import re
#
# class CustomConverter(DefaultConverter):
#
#     @DefaultConverter.convert_method('catalog.Product')
#     def convert_product(self, value, parameter, task):
#         from catalog.models import Product
#         try:
#             self.product = BulkProduct.objects.get(id=value)
#             return self.product
#         except Product.DoesNotExist:
#             raise Http404('Product "{}" not found.'.format(value))
#
# # set as the default for all view functions
# set_default_converter(CustomConverter)
