from .models import ToDoItemList
from django.forms import ModelForm, TextInput, EmailInput, NumberInput, Textarea, DateTimeInput



class ToDoItemForm(ModelForm):
    class Meta:
        model = ToDoItemList
        fields= ["todo_list", "title", "description", "due_date", "priority", "item_completed"]
        widgets = {
            'due_date': DateTimeInput(attrs={'class':"form-control", 'type':'date'}),
        }

