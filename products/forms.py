from django import forms
from .models import getProductGroupChoices, ProductGroup, Product, Purchase, PRODUCT_CHOICES_FOR_SEARCH, CURRENCIES
from customers.models import Customer, Supplier
from sales.forms import CHART_CHOICES, MONTH_SELECT, current_year, current_month, year_choices

PURCHASE_SUM_CHOICES = (
    ('quantity', 'Quantity'),
    ('added_price_KRW', 'Purchase Price_KRW'),
    ('added_price', 'Purchase Price'),
)

PRODUCT_SUM_CHOICES = (
    ('inventory', 'Inventory'),
    ('average_unit_price_KRW', 'Average Unit Price_KRW'),
    #('total_quantity', 'Total quantity'),
    #('total_added_price_KRW', 'Total Purchase Cost'),
)

class ProductGroupForm(forms.ModelForm):
    class Meta:
        model = ProductGroup
        fields= ["name", 'remark']

class ProductForm(forms.ModelForm):
    customers = forms.ModelMultipleChoiceField(
        queryset=Customer.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    supplier = forms.ModelChoiceField(
        widget=forms.RadioSelect,
        queryset=Supplier.objects.all(),
    )

    currency = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=CURRENCIES,
    )
    
    product_type = forms.ModelChoiceField(
        widget=forms.RadioSelect,
        queryset=ProductGroup.objects.all(),
    )

    class Meta:
        model = Product
        fields= ["name", 'currency', "price",  'moq', 'price_quantity_base', 'supplier', 'customers', 'remark', 'product_type', 'image']

class ProductSearchForm(forms.Form):
    chart_type = forms.ChoiceField(choices=CHART_CHOICES, widget=forms.Select(attrs={'style':'width: 100%'}))
    type_by = forms.ModelChoiceField(
        widget = forms.RadioSelect,
        queryset=ProductGroup.objects.all(),
        required = False,
        )
    sum_by = forms.ChoiceField(choices=PRODUCT_SUM_CHOICES, widget=forms.Select(attrs={'style':'width: 100%'}))
    supplier_by = forms.ModelChoiceField(
        widget=forms.RadioSelect,
        queryset=Supplier.objects.all(),
        required = False,
        )

class PurchaseForm(forms.ModelForm):
    product = forms.ModelChoiceField(
            widget=forms.RadioSelect,
            queryset=Product.objects.all(),
        )

    class Meta:
        model = Purchase
        fields= ["product", "unit_price", "quantity", "added_cost", "ex_rate_to_KRW", "custom_tax_KRW", 'transport_cost_KRW', "bank_cost_KRW", "delivery_cost_KRW", "status"]

class PurchaseSearchForm(forms.Form):
    date_from = forms.DateField(widget=forms.DateInput(attrs={'type':'date', 'style':'width: 50%', 'autofocus':True}), required=False)
    date_to = forms.DateField(widget=forms.DateInput(attrs={'type':'date', 'style':'width: 50%'}), required=False)
    year_from = forms.TypedChoiceField(coerce=int, choices=year_choices, initial=current_year, required=False)
    year_to = forms.TypedChoiceField(coerce=int, choices=year_choices, initial=0, required=False)
    month_from = forms.TypedChoiceField(coerce=int, choices=MONTH_SELECT, initial=current_month, required=False)
    month_to = forms.TypedChoiceField(coerce=int, choices=MONTH_SELECT, initial=0, required=False)
    chart_type = forms.ChoiceField(choices=CHART_CHOICES, widget=forms.Select(attrs={'style':'width: 100%'}))

    results_by = forms.ModelChoiceField(
        widget = forms.RadioSelect,
        queryset=ProductGroup.objects.all(),
        required = False,
        )

    sum_by = forms.ChoiceField(choices=PURCHASE_SUM_CHOICES, widget=forms.Select(attrs={'style':'width: 100%'}))
