from django import forms
from .models import Product, PRODUCT_CHOICES_FOR_SEARCH
from sales.forms import CHART_CHOICES
from django.forms import ModelForm, TextInput, EmailInput, NumberInput, Textarea, DateTimeInput, DateInput, Select

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields= ["name", "price", 'remark', 'product_type', 'image']

class ProductSearchForm(forms.Form):
    chart_type = forms.ChoiceField(choices=CHART_CHOICES, widget=forms.Select(attrs={'style':'width: 100%'}))
    results_by = forms.ChoiceField(choices=PRODUCT_CHOICES_FOR_SEARCH, widget=forms.Select(attrs={'style':'width: 100%'}))
