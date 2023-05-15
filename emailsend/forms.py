# ContactUs will be e-mailed back to the admin as an email form rather than model-based form
from django import forms
from django.conf import settings
from django.core.mail import send_mail
from django.db import models

#from django.forms import ModelForm, TextInput, EmailInput, NumberInput, Textarea
#from .models import ContactUs
#from django.forms import ModelForm, TextInput, EmailInput, NumberInput, Textarea

class ContactForm(forms.Form):
#    your_first_Name = forms.CharField(max_length=64, required=True, widget=forms.TextInput(attrs={'size':'100%)', 'autofocus':True}))
#    your_last_Name = forms.CharField(max_length=64, required=True, widget=forms.TextInput(attrs={'size':'100%)'}))
#    your_email_Address = forms.EmailField(max_length=128, required=True, widget=forms.TextInput(attrs={'size':'100%)'}))
    subject = forms.CharField(max_length=128, widget=forms.TextInput(attrs={'size':'100%)', 'autofocus':True}))
    to = forms.CharField(max_length=256, required=True, widget=forms.TextInput(attrs={'size':'100%)'}))
    cc = forms.CharField(max_length=256, required=False, widget=forms.TextInput(attrs={'size':'100%)'}))
    bcc = forms.CharField(max_length=256, required=False, widget=forms.TextInput(attrs={'size':'100%)'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'rows':10, 'cols':98}))
    attach = forms.FileField(required=False, widget=forms.ClearableFileInput(attrs={'multiple': True}))

"""
class ContactUsForm(ModelForm):
    class Meta:
        model= ContactUs
        fields= ["first_Name", "last_Name", "email_Address", "phone_Number", "contact_Message"]
        widgets = {
            'first_Name': TextInput(attrs={
                'class': "form-control",
                'style': 'min-width: 100%; border-style: none none solid none; border-color: blue;',
                }),
            'last_Name': TextInput(attrs={
                'class': "form-control",
                'style': 'min-width: 100%; border-style: none none solid none; border-color: blue;',
                }),
            'email_Address': EmailInput(attrs={
                'class': "form-control", 
                'style': 'min-width: 100%; border-style: none none solid none; border-color: blue;',
                }),
            'phone_Number': TextInput(attrs={
                'class': "form-control",
                'style': 'min-width: 100%; border-style: none none solid none; border-color: blue;',
                }),
            'contact_Message': Textarea(attrs={
                'class': "form-control", 
                'style': 'min-width: 100%; border-style: none none solid none; border-color: blue;',
                })
        }
"""