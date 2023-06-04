from django import forms
from .models import Bulletin
from django.forms import ModelForm, TextInput, EmailInput, NumberInput, Textarea, DateTimeInput, DateInput, Select

class PostForm(forms.ModelForm):
    class Meta:
        model = Bulletin
        fields= ['title', 'content']

