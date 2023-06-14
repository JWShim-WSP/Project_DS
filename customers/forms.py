from django import forms
from .models import Customer, Supplier

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields= ["name", "email", "cc", "phone_number", "remark", "logo"]

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields= ["name", "email", "cc", "phone_number", "remark", "logo"]
