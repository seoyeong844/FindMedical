from django import forms

class SearchForm(forms.Form):
    check_values = forms.BooleanField(required=False)
