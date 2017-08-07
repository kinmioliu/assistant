from django import forms

class TDS_GetVerform(forms.Form):
    name = forms.CharField()

class VersionFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()

