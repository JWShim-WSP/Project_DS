from django import forms
from profiles.models import Profile

class MemberForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields= ["user", "bio", "avatar"]

