from .models import Event
from django.forms import ModelForm, TextInput, EmailInput, NumberInput, Textarea, DateTimeInput



class EventForm(ModelForm):
    class Meta:
        model = Event
        fields= ["title", "description", "start_date", "end_date", "event_completed"]
        widgets = {
            'start_date': DateTimeInput(attrs={'class':"form-control", 'type':'date'}),
            'end_date': DateTimeInput(attrs={'class':"form-control",'type':'date'}),
        }
