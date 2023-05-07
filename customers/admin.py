from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin
from customers.resources import CustomerResource
from .models import Customer

# Register your models here.

class CustomerAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    resource_class = CustomerResource
    list_display = ("name", "logo")


admin.site.register(Customer, CustomerAdmin)