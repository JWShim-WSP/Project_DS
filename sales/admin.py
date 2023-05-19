from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin
from sales.resources import PositionResource, SaleResource
from .models import Position, Sale, CSV

# Register your models here.
class PositionAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    resource_class = PositionResource

class SaleAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    resource_class = SaleResource

admin.site.register(Position, PositionAdmin)
admin.site.register(Sale, SaleAdmin)
admin.site.register(CSV)