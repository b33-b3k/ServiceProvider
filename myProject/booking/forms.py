from django import forms
from .models import VendorRequest

class VendorRequestForm(forms.ModelForm):
    class Meta:
        model = VendorRequest
        fields = [
            'business_name',
            'business_address',
            'contact_number',
            'email',
            'business_description',
            'business_category',
            'pan_number',
        ]
