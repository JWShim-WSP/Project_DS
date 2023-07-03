from django.contrib import admin
from .models import ProductGroup, Product, Purchase
from import_export.admin import ImportExportActionModelAdmin
from products.resources import ProductGroupResource, ProductResource, PurchaseResource

# Register your models here.
class ProductGroupAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    resource_class = ProductGroupResource

class ProductAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    resource_class = ProductResource

class PurchaseAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    resource_class = PurchaseResource

admin.site.register(ProductGroup, ProductGroupAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Purchase, PurchaseAdmin)
