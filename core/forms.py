from django import forms
from .models import *

class VoteForm(forms.ModelForm):
    class Meta:
        model = Vote
        exclude = ('user',)