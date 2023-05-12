from django import forms

CHART_CHOICES = (
    ('#1', 'Bar Chart'),
    ('#2', 'Bar Horizontal Chart'),
    ('#3', 'Pie Chart'),
    ('#4', 'Line Chart'),
)

RESULT_CHOICES = (
    ('#1', 'transaction'),
    ('#2', 'position'),
    ('#3', 'sales date'),
    ('#4', 'customer'),
    ('#5', 'salesman'),
)

class SalesSearchForm(forms.Form):
    date_from = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    date_to = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    chart_type = forms.ChoiceField(choices=CHART_CHOICES)
    results_by = forms.ChoiceField(choices=RESULT_CHOICES)    