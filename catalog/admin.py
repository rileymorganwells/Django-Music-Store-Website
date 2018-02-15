from django.contrib import admin
from catalog import models as cmod

# Register your models here.
admin.site.register(cmod.Product)
admin.site.register(cmod.Category)
