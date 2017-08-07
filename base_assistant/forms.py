from django import forms;
class TDS_GetVerform(forms):
    text = forms.CharFiled(widget=forms.TextAreas())
    print(text)
