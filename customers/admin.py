from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin
from customers.resources import CustomerResource, SupplierResource
from .models import Customer, Supplier

# Register your models here.

class CustomerAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    resource_class = CustomerResource
    list_display = ("name", "logo")

class SupplierAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    resource_class = SupplierResource
    list_display = ("name", "logo")

admin.site.register(Customer, CustomerAdmin)
admin.site.register(Supplier, SupplierAdmin)