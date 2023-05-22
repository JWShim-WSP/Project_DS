from django import forms
from .models import Product, PRODUCT_CHOICES_FOR_SEARCH
from django.forms import ModelForm, TextInput, EmailInput, NumberInput, Textarea, DateTimeInput, DateInput, Select

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields= ["name", "price", 'remark', 'product_type', 'image']

CHART_CHOICES = (
    ('Bar Chart', 'Bar Chart'),
    ('Horizontal Bar Chart', 'Horizontal Bar Chart'),
    ('Pie Chart', 'Pie Chart'),
    ('Line Chart', 'Line Chart'),
)

class ProductSearchForm(forms.Form):
    chart_type = forms.ChoiceField(choices=CHART_CHOICES, widget=forms.Select(attrs={'style':'width: 25%'}))
    results_by = forms.ChoiceField(choices=PRODUCT_CHOICES_FOR_SEARCH, widget=forms.Select(attrs={'style':'width: 25%'}))
