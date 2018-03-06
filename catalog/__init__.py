# All apps that are DMP-enabled must have this setting in their app-level __init__.py
DJANGO_MAKO_PLUS = True

# from django_mako_plus import set_default_converter, DefaultConverter
# from catalog import models as cmod
# from catalog.models import Category
#
# class CustomConverter(DefaultConverter):
#
#     @DefaultConverter.convert_method()
#     def convert_category(self, selection:cmod.Category):
#         if selection is none:
#             return selection(name='All Products')
#
# # set as the default for all view functions
# set_default_converter(CustomConverter)
