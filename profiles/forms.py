from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    bio = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 7, 'cols': '100%'}))

    class Meta:
        model = Profile
        fields= ["first_name", "last_name", "bio", "email", "language", "menubar", "licensed_by", "avatar"]


# to export a file
FORMAT_CHOICES = (
    ('xls', 'xls'),
    ('csv', 'csv'),
    ('json', 'json'),
)
class FormatForm(forms.Form):
    format = forms.ChoiceField(choices=FORMAT_CHOICES, widget=forms.Select(attrs={'class':'form-select'}))
