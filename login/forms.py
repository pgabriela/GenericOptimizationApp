from django import forms
from .models import LoginData


class LoginForm(forms.ModelForm):
    class Meta:
        model = LoginData
        fields = ('Username', 'Password',)
