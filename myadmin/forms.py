from django import forms
from profiles.models import Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class MemberForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'is_staff')


class NewMemberForm(UserCreationForm):
   email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.', required=True)
   class Meta:
      model = User
      fields = ('username', 'first_name', 'last_name', 'password1', 'password2', 'email', 'is_staff')


