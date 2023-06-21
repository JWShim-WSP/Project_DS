from django.contrib import admin

# Register your models here.

# No need to have db for Contactus which will be sent to email directly
"""
from .models import ContactUs

class ContactAdmin(admin.ModelAdmin):
    list_display = ("first_Name", "last_Name", "email_Address", "phone_Number", "contact_Date", "contact_Message")

admin.site.register(ContactUs, ContactAdmin)
"""