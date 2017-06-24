from django import forms
from .models import ProjectGroup


class InviteFriendForm(forms.Form):
    username = forms.CharField(label="Your Friend's Username", max_length=100)


class MakeGroupForm(forms.ModelForm):

    class Meta:
        model = ProjectGroup
        fields = ('projectname', 'inTopic',)


class MakePrefsForm(forms.Form):
    pass
