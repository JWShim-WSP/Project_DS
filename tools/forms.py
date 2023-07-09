from django import forms

# The first value is for the choice value, the second value is used for displaying in the form
LANGUAGE_CHOICES = (
    ('English', 'English'),
    ('Korea', 'Korean'),
    ('Spanish', 'Spanish'),
    ('German', 'German'),
    ('French', 'French'),
    ('Japanese', 'Japanese'),
)

class GeneralQuestionForm(forms.Form):
    Prompt = forms.CharField(max_length=1024, required=True, widget=forms.TextInput(attrs={'size':'100%'}))

class TranslationRequestForm(forms.Form):
    Prompt = forms.CharField(max_length=1024, required=True, widget=forms.TextInput(attrs={'size':'100%'}))
    To_language = forms.ChoiceField(choices=LANGUAGE_CHOICES, widget=forms.Select(attrs={'style':'width: 100%'}))

class ImageRequestForm(forms.Form):
    Prompt = forms.CharField(max_length=1024, required=True, widget=forms.TextInput(attrs={'size':'100%'}))
