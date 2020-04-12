from django import forms

class user_input(forms.Form):
    Company_name = forms.CharField()
    Ticker_symbol = forms.CharField()
