from django import forms


class DivForm(forms.Form):
    textarea = forms.CharField(widget=forms.Textarea(attrs={'rows': 15, 'cols': 10}), label='')