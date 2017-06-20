from django import forms


class InviteFriendForm(forms.Form):
    username = forms.CharField(label="Your Friend's Username", max_length=100)
