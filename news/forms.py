from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from captcha.fields import CaptchaField
from django import forms
from .models import NewspaperIssue

class CustomUserCreationForm(UserCreationForm):
    captcha = CaptchaField(label="Please input your captcha")

    class Meta:
        model = User
        fields = ("username", "password1", "password2")



class NewspaperIssueForm(forms.ModelForm):
    class Meta:
        model = NewspaperIssue
        fields = ['title', 'content', 'editors', 'topics', 'photo']
        widgets = {
            'topics': forms.CheckboxSelectMultiple(),
        }
