from django import forms
from django.forms import ModelForm
from . models import *

class Loginform(forms.Form):    
    email = forms.EmailField(widget=forms.TextInput(
    attrs={"class": "form-control", "placeholder": "Email"}))
    phone = forms.CharField(widget=forms.TextInput(
    attrs={"class": "form-control", "placeholder": "Phone"}))
    
class grade_form(forms.ModelForm):
    
    class Meta:
        model = Grade
        fields = '__all__'

class subject_form(forms.ModelForm):
    
    class Meta:
        model = Subject
        fields = '__all__'

class chapter_form(forms.ModelForm):
    class Meta:
        model = Chapter
        fields = '__all__'
        
class chapterlist_form(forms.Form):
    grade= forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "grade"}))
    subject= forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "subject"}))
    
    
class question_form(forms.ModelForm):
    class Meta:
        model = Question
        fields = '__all__'
