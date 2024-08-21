from django import forms
from .models import ContactForm

class WebsiteContactForm(forms.ModelForm):

    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete':'off', 'placeholder': 'Your Name'})) 
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'autocomplete':'off', 'placeholder':'Email'}))
    subject = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete':'off', 'placeholder':'Subject'})) 
    message = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete':'off', 'placeholder':'Message'})) 

    class Meta:
        model = ContactForm
        fields = ['name', 'email', 'subject', 'message']
