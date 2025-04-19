from django.contrib.auth.models import User
from django import forms

class CreateUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    birth_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password']