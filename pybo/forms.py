from django import forms
from .models import *


class QuestionForm(forms.ModelForm):

    class Meta:
        model = Question
        fields = ("subject", "content")


class AnswerForm(forms.ModelForm):

    class Meta:
        model = Answer
        fields = ("content",)
        label = {"content": "답변 내용"}
