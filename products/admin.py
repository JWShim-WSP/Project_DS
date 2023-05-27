from django.contrib import admin
from .models import Product
from import_export.admin import ImportExportActionModelAdmin
from products.resources import ProductResource

# Register your models here.
class ProductAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    resource_class = ProductResource

admin.site.register(Product, ProductAdmin)
