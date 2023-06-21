from .models import ToDoItemList, ToDoList
from django.forms import ModelForm, TextInput, EmailInput, NumberInput, Textarea, DateTimeInput, DateInput, Select


class ToDoForm(ModelForm):
    class Meta:
        model = ToDoList
        fields= ["title", "priority"]
        widgets = {
            'title': TextInput(attrs={'class':"form-control", 'autofocus':True}),
            'priority': Select(attrs={'class':"form-control", 'style':'width: 25%'})
        }


class ToDoItemForm(ModelForm):
    class Meta:
        model = ToDoItemList
        fields= ["todo_list", "title", "description", "due_date", "priority", "item_completed"]
        widgets = {
            'todo_list': Select(attrs={'class':"form-control", 'autofocus':True}),
            'due_date': DateInput(attrs={'class':"form-control", 'type':'date', 'style':'width: 25%'}),
            'priority': Select(attrs={'class':"form-control", 'style':'width: 25%'})
        }

