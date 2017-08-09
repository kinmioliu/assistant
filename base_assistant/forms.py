from django import forms

class TDS_GetVerform(forms.Form):
    name = forms.CharField()

class VersionFileForm(forms.Form):
    verinfo_file = forms.FileField()

