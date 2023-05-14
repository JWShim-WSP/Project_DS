from .models import Event
from django.forms import ModelForm, TextInput, EmailInput, NumberInput, Textarea, DateInput



class EventForm(ModelForm):
    class Meta:
        model = Event
        fields= ["title", "description", "start_date", "end_date", "event_completed"]
        widgets = {
            'title': TextInput(attrs={'class':"form-control", 'autofocus':True}),
            'start_date': DateInput(attrs={'class':"form-control", 'type':'date', 'style':'width: 25%' }),
            'end_date': DateInput(attrs={'class':"form-control",'type':'date', 'style':'width: 25%'}),
        }
