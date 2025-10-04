from django import forms
from .models import Salesman

class SalesmanForm(forms.ModelForm):
    class Meta:
        model = Salesman
        fields = ['name', 'address', 'phone', 'email']
