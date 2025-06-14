from django import forms
from .models import Contact

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'phone', 'email', 'city', 'state']
        help_texts = {
            'phone': None  # This removes the help text
        }