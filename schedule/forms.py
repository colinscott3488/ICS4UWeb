from django import forms
from django.contrib.auth.models import User

class NavigationForm(forms.Form):
    DIRECTION_CHOICES = [
        ('back', 'Go Back'),
        ('current', 'Current Date'),
        ('forward', 'Go Forward'),
    ]

    direction = forms.ChoiceField(choices=DIRECTION_CHOICES, widget=forms.RadioSelect)

class scheduleCreate(forms.Form):
    users = forms.ModelChoiceField(queryset=User.objects.all(), empty_label=None, widget=forms.Select(attrs={'class': 'form-control'}))
    weekStart = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))