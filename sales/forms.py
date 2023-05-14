from django import forms

CHART_CHOICES = (
    ('#1', 'Bar Chart'),
    ('#2', 'Bar Horizontal Chart'),
    ('#3', 'Pie Chart'),
    ('#4', 'Line Chart'),
)

RESULT_CHOICES = (
    ('#1', 'transaction'),
    ('#2', 'product'),
    ('#3', 'position'),
    ('#4', 'sales date'),
    ('#5', 'customer'),
    ('#6', 'salesman'),
)

SUM_CHOICES = (
    ('#1', 'price'),
    ('#2', 'quantity'),
)


class SalesSearchForm(forms.Form):
    date_from = forms.DateField(widget=forms.DateInput(attrs={'type':'date', 'style':'width: 25%', 'autofocus':True}))
    date_to = forms.DateField(widget=forms.DateInput(attrs={'type':'date', 'style':'width: 25%'}))
    chart_type = forms.ChoiceField(choices=CHART_CHOICES, widget=forms.Select(attrs={'style':'width: 25%'}))
    results_by = forms.ChoiceField(choices=RESULT_CHOICES, widget=forms.Select(attrs={'style':'width: 25%'}))
    sum_by = forms.ChoiceField(choices=SUM_CHOICES, widget=forms.Select(attrs={'style':'width: 25%'}))