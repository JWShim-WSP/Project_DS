from django.forms import ModelForm, TextInput
from .models import Report

class ReportForm(ModelForm):
    class Meta:
        model = Report
        fields = ('name', 'remarks')
        widgets = {
            'name': TextInput(attrs={'class':"form-control", 'autofocus':True})
        }