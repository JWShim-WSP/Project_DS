from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin
from reports.resources import ReportResource
from .models import Report

# Register your models here.
class ReportAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    resource_class = ReportResource
    list_display = ("name", "remarks", "author", "created", "updated")

admin.site.register(Report, ReportAdmin)