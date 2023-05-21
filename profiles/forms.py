from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields= ["bio", "language", "menubar", "licensed_by", "avatar"]


# to export a file
FORMAT_CHOICES = (
    ('xls', 'xls'),
    ('csv', 'csv'),
    ('json', 'json'),
)
class FormatForm(forms.Form):
    format = forms.ChoiceField(choices=FORMAT_CHOICES, widget=forms.Select(attrs={'class':'form-select'}))
