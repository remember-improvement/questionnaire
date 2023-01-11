from pyexpat import model
from questionnaire.models import Answer
from django import forms

class AnswerPostForm(forms.Form):
    answer = forms.CharField(label='answer',max_length=32,required=True)


class LoginPostForm(forms.Form):
    username = forms.CharField(label='username',max_length=32,required=True)
    bankaccount = forms.CharField(label='bandaccount',max_length=64,required=True)