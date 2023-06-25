from django import forms
from .models import Sale, Position
from products.models import Product
from products.models import PRODUCT_CHOICES_FOR_SEARCH
from django.forms import ModelForm, TextInput, EmailInput, NumberInput, Textarea, DateTimeInput, DateInput, Select
import datetime
from django.core.validators import MaxValueValidator, MinValueValidator

# The first value is for the choice value, the second value is used for displaying in the form
CHART_CHOICES = (
    ('Horizontal Bar Chart', 'Horizontal Bar Chart'),
    ('Pie Chart', 'Pie Chart'),
    ('Line Chart', 'Line Chart'),
    ('Bar Chart', 'Bar Chart'),
)

RESULT_CHOICES = (
    ('product', 'Product'),
    ('customer', 'Customer'),
    ('salesman', 'Salesman'),
    ('created', 'Sales date'),
    ('year', 'Yearly'),
    ('year_month', 'Year-Monthly'),
    ('position_id', 'Position'),
    ('transaction_id', 'Transaction'),
)

SALES_SUM_CHOICES = (
    ('total_net_price', 'Sales Price'), # Position' added_price_KRW should be used instead of 'total_added_price_KRW' of Sale
    ('final_profit', 'Final Profit'), # Position' added_price should be used instead of 'total_added_price' of Sale
    ('net_profit', 'Sales Profit'),
)

POSITION_SUM_CHOICES = (
    ('net_price', 'Sales Price'), # Position' added_price_KRW should be used instead of 'total_added_price_KRW' of Sale
    ('margin_percentage', 'Margin Percentage'), # Position' added_price should be used instead of 'total_added_price' of Sale
    ('quantity', 'Quantity'),
)


MONTH_SELECT = [
    (0, ""),
    (1, 'January'),
    (2, 'February'),
    (3, 'March'),
    (4, 'April'),
    (5, 'May'),
    (6, 'June'),
    (7, 'July'),
    (8, 'August'),
    (9, 'September'),
    (10, 'October'),
    (11, 'November'),
    (12, 'December'),
]

def current_year():
    return datetime.date.today().year

def current_month():
    return datetime.date.today().month

def year_choices():
    year_list = [(r,r) for r in range(2010, datetime.date.today().year+1)]
    year_list.insert(0, (0, ""))
    return year_list


class SalesSearchForm(forms.Form):
    date_from = forms.DateField(widget=forms.DateInput(attrs={'type':'date', 'style':'width: 50%', 'autofocus':True}), required=False)
    date_to = forms.DateField(widget=forms.DateInput(attrs={'type':'date', 'style':'width: 50%'}), required=False)
    year_from = forms.TypedChoiceField(coerce=int, choices=year_choices, initial=current_year, required=False)
    year_to = forms.TypedChoiceField(coerce=int, choices=year_choices, initial=0, required=False)
    month_from = forms.TypedChoiceField(coerce=int, choices=MONTH_SELECT, initial=current_month, required=False)
    month_to = forms.TypedChoiceField(coerce=int, choices=MONTH_SELECT, initial=0, required=False)
    chart_type = forms.ChoiceField(choices=CHART_CHOICES, widget=forms.Select(attrs={'style':'width: 100%'}))
    results_by = forms.ChoiceField(choices=RESULT_CHOICES, widget=forms.Select(attrs={'style':'width: 100%'}))
    sum_by = forms.ChoiceField(choices=SALES_SUM_CHOICES, widget=forms.Select(attrs={'style':'width: 100%'}))

class PositionSearchForm(forms.Form):
    date_from = forms.DateField(widget=forms.DateInput(attrs={'type':'date', 'style':'width: 50%', 'autofocus':True}), required=False)
    date_to = forms.DateField(widget=forms.DateInput(attrs={'type':'date', 'style':'width: 50%'}), required=False)
    year_from = forms.TypedChoiceField(coerce=int, choices=year_choices, initial=current_year, required=False)
    year_to = forms.TypedChoiceField(coerce=int, choices=year_choices, initial=0, required=False)
    month_from = forms.TypedChoiceField(coerce=int, choices=MONTH_SELECT, initial=current_month, required=False)
    month_to = forms.TypedChoiceField(coerce=int, choices=MONTH_SELECT, initial=0, required=False)
    chart_type = forms.ChoiceField(choices=CHART_CHOICES, widget=forms.Select(attrs={'style':'width: 100%'}))
    results_by = forms.ChoiceField(choices=PRODUCT_CHOICES_FOR_SEARCH, widget=forms.Select(attrs={'style':'width: 100%'}))
    sum_by = forms.ChoiceField(choices=POSITION_SUM_CHOICES, widget=forms.Select(attrs={'style':'width: 100%'}))

class CustomPositionChoice(forms.ModelMultipleChoiceField):
    def label_from_instance(self, position):
        return "%s" %position.id

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields= ['positions', "tax_cost", "vat_cost", 'delivery_cost', 'extra_cost', 'customer', 'salesman']
    
    positions = forms.ModelMultipleChoiceField(
        queryset=Position.objects.filter(inventory_status=True, position_sold=False),
        widget=forms.CheckboxSelectMultiple
    )

class ExecutedSaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields= ['positions', "tax_cost", "vat_cost", 'delivery_cost', 'extra_cost', 'customer', 'salesman']

    positions = forms.ModelMultipleChoiceField(
        queryset=Position.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )
   


# You can modify the 'Choice of positions' with different names
#class CustomMMPosition(forms.ModelMultipleChoiceField):
#    def label_from_instance(self, position):
#        return "%s" % position.product.name
#    
#class SaleForm(forms.ModelForm):
#    class Meta:
#        model = Sale
#        fields= ["transaction_id", "positions", "total_net_price", "total_added_price", "total_net_price_KRW", "total_added_price_KRW", "customer", 'salesman']
#
#    positions = CustomMMPosition(
#        queryset=Position.objects.all(),
#        widget=forms.CheckboxSelectMultiple
#    )

class PositionForm(forms.ModelForm):
    product = forms.ModelChoiceField(
            widget=forms.RadioSelect,
            queryset=Product.objects.all(),
        )

    class Meta:
        model = Position
        fields= ["product", "unit_price", "quantity"]
