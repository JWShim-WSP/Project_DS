from django import forms

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
    ('price', 'price'),
    ('quantity', 'quantity'),
)


class SalesSearchForm(forms.Form):
    date_from = forms.DateField(widget=forms.DateInput(attrs={'type':'date', 'style':'width: 25%', 'autofocus':True}))
    date_to = forms.DateField(widget=forms.DateInput(attrs={'type':'date', 'style':'width: 25%'}))
    chart_type = forms.ChoiceField(choices=CHART_CHOICES, widget=forms.Select(attrs={'style':'width: 25%'}))
    results_by = forms.ChoiceField(choices=RESULT_CHOICES, widget=forms.Select(attrs={'style':'width: 25%'}))
    sum_by = forms.ChoiceField(choices=SUM_CHOICES, widget=forms.Select(attrs={'style':'width: 25%'}))