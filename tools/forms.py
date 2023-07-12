from django import forms
from .models import GeneralQuestion, TranslationQuestion, Image
from .models import LANGUAGE_CHOICES 

class GeneralQuestionForm(forms.ModelForm):
    prompt = forms.CharField(max_length=512, required=True, widget=forms.TextInput(attrs={'size':'99%', 'autofocus': True}))
    class Meta:
        model = GeneralQuestion
        fields = ["prompt"]


class TranslationQuestionForm(forms.ModelForm):
    prompt = forms.CharField(max_length=512, required=True, widget=forms.TextInput(attrs={'size':'99%', 'autofocus': True}))
    to_other_language = forms.CharField(max_length=512, required=False, widget=forms.TextInput(attrs={'size':'99%'}))
    class Meta:
        model=TranslationQuestion
        fields = ["prompt", "to_language", "to_other_language"]


class ImageRequestForm(forms.ModelForm):
    prompt = forms.CharField(max_length=1024, required=True, widget=forms.TextInput(attrs={'size':'99%', 'autofocus': True}))
    class Meta:
        model = Image
        fields = ["prompt"]
