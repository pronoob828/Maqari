from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from phonenumber_field.formfields import PhoneNumberField

from account.models import Account


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        max_length=60, help_text="Required. Add a valid email adress"
    )

    phone_num = PhoneNumberField()
    class Meta:
        model = Account
        fields = ("email", "username", "password1", "password2", "last_name",
                  "phone_num", "gender", "current_residence", "nationality")


class AccountAuthenticationForm(forms.ModelForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ("email", "password")

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data["email"]
            password = self.cleaned_data["password"]
            if not authenticate(email=email, password=password):
                raise forms.ValidationError(
                    "Invalid Login. Make sure you activated your account.")
