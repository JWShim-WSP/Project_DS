from django.contrib import admin
from .models import Product, Purchase
from import_export.admin import ImportExportActionModelAdmin
from products.resources import ProductResource, PurchaseResource

# Register your models here.
class ProductAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    resource_class = ProductResource

class PurchaseAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    resource_class = PurchaseResource

admin.site.register(Product, ProductAdmin)
admin.site.register(Purchase, PurchaseAdmin)
