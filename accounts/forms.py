from django import forms
from django.forms import ModelForm
from . models import *

class signup(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Email"}))
    register_number = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Register Number"}))
    date_of_birth = forms.DateField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Date of Birth"}))
    user_type = forms.ChoiceField(choices=usertype_choice)
    phone = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Phone"}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "First Name"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Last Name"}))
    full_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Fullname"}))
    address = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Address"}))
    standard = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Standard"}))
    section = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Section"}))
    data_entry_user = forms.BooleanField(required=False)


class login_form(forms.ModelForm):
    
    class Meta:
        model = User
        fields = {'email','phone'}