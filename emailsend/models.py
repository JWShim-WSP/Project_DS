#from django.db import models
#from django import forms

# Create your models here. Send email instead of Save contact message
"""
No model needed to save in db. 
class ContactUs(models.Model):
    first_Name = models.CharField(max_length=64, blank = False)
    last_Name = models.CharField(max_length=64, blank = False)
    email_Address = models.EmailField(null=True, blank = False)
    phone_Number = models.CharField(max_length=64, blank=True)
    contact_Message = models.TextField(max_length=1024, blank=False)
    contact_Date = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f"{self.first_Name} {self.last_Name}"
"""
