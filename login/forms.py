from django.contrib.auth.forms import AuthenticationForm


class LoginForm(AuthenticationForm):
    fields = ("username", "password",)
