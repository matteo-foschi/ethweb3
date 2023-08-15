from django import forms
from .models import Survey


class SurveyForm(forms.ModelForm):
    email = forms.CharField(max_length=100, required=True)
    receipt = forms.CharField(max_length=100, required=True)
    receiptAmount = forms.FloatField(required=True)

    class Meta:
        model = Survey
        fields = ("email", "receipt", "receiptAmount")
