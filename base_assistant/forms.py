from django import forms
from base_assistant.models import VersionInfo

class TDS_GetVerform(forms.Form):
    name = forms.CharField()

class VersionFileForm(forms.Form):
    verinfo_file = forms.FileField()

class VerinfoFileFormModel(forms.ModelForm):
    class Meta:
        model = VersionInfo
        fields = ['product', 'platform_ver', 'product_ver', 'verinfo']


