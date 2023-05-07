from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin
from profiles.resources import MemberResource
from .models import Profile

# Register your models here.
class ProfileAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    resource_class = MemberResource
    list_display = ("user", "bio", "avatar", "created", "updated")


admin.site.register(Profile, ProfileAdmin)