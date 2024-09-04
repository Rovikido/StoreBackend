from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
import re

from .models import CustomerUser

class CustomerUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomerUser
        fields = ('username', 'email', 'first_name', 'last_name', 'phone_number', 'delivery_address')
    
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if phone_number and not re.match(r'^\+?1?\d{9,15}$', phone_number):
            raise ValidationError("Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
        return phone_number


class CustomerUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = CustomerUser
        fields = ('username', 'email', 'first_name', 'last_name', 'phone_number', 'delivery_address')

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if phone_number and not re.match(r'^\+?1?\d{9,15}$', phone_number):
            raise ValidationError("Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
        return phone_number
