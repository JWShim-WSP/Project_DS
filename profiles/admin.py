from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin
from profiles.resources import ProfileResource
from .models import Profile, Relationship

# Register your models here.
class ProfileAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    resource_class = ProfileResource
    list_display = ("user", "bio", "avatar", "created", "updated")


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Relationship)