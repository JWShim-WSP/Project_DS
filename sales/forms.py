from django import forms
from .models import Sale, Position
from django.forms import ModelForm, TextInput, EmailInput, NumberInput, Textarea, DateTimeInput, DateInput, Select

# The first value is for the choice value, the second value is used for displaying in the form
CHART_CHOICES = (
    ('Bar Chart', 'Bar Chart'),
    ('Horizontal Bar Chart', 'Horizontal Bar Chart'),
    ('Pie Chart', 'Pie Chart'),
    ('Line Chart', 'Line Chart'),
)

RESULT_CHOICES = (
    ('transaction_id', 'Transaction'),
    ('product', 'Product'),
    ('position_id', 'Position'),
    ('created', 'Sales date'),
    ('customer', 'Customer'),
    ('salesman', 'Salesman'),
)

SUM_CHOICES = (
    ('added_price', 'price'),
    ('quantity', 'quantity'),
)

class SalesSearchForm(forms.Form):
    date_from = forms.DateField(widget=forms.DateInput(attrs={'type':'date', 'style':'width: 25%', 'autofocus':True}))
    date_to = forms.DateField(widget=forms.DateInput(attrs={'type':'date', 'style':'width: 25%'}))
    chart_type = forms.ChoiceField(choices=CHART_CHOICES, widget=forms.Select(attrs={'style':'width: 25%'}))
    results_by = forms.ChoiceField(choices=RESULT_CHOICES, widget=forms.Select(attrs={'style':'width: 25%'}))
    sum_by = forms.ChoiceField(choices=SUM_CHOICES, widget=forms.Select(attrs={'style':'width: 25%'}))

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields= ["transaction_id", "positions", "total_net_price", "total_added_price", "total_net_price_KRW", "total_added_price_KRW", "customer", 'salesman']

class PositionForm(forms.ModelForm):
    class Meta:
        model = Position
        fields= ["product", "quantity", "unit_price", "added_cost", "net_price", "added_price", "ex_rate_to_KRW", "added_cost_KRW", "net_price_KRW", "added_price_KRW"]
