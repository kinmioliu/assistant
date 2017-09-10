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

class SearchForm(forms.Form):
    query = forms.CharField(label='cfg-add-board', widget=forms.TextInput(attrs={'size':32, 'class':'form-control'}))

class PolicyFileForm(forms.Form):
    """策略"""
    policy_file = forms.FileField()

class MMLFileForm(forms.Form):
    """策略"""
    mml_file = forms.FileField()