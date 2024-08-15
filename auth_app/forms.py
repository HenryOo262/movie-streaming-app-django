from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password1','password2']

    username = forms.CharField(
        label='Username'
    )


class LoginForm(forms.Form):    # authenticate() problem with ModelForm
    username = forms.CharField(
        label='Username',
        widget=forms.TextInput()
    )

    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput()
    )


class ProfileForm(forms.Form):  # problem with modelForm
    username = forms.CharField(
        label='Username',
        widget=forms.TextInput()
    )

    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput()
    )

    first_name = forms.CharField(
        label="First name",
        widget=forms.TextInput()
    )

    last_name = forms.CharField(
        label="Last name",
        widget=forms.TextInput()
    )


'''
class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password']

    username = forms.CharField(
        label='Username'
    )

    email = forms.EmailField(
        widget=forms.EmailInput()
    )

    password = forms.CharField(
        widget=forms.PasswordInput()
    )

    repeat_password = forms.CharField(
        label='Retype Password',
        widget=forms.PasswordInput()
    )

    def clean_password(self):
        value = self.cleaned_data.get('password')
        if len(value) < 8:
            raise forms.ValidationError('Password must have at least 8 characters')
        return value

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        repeat_password = cleaned_data.get('repeat_password')
        if not password == repeat_password:
            raise forms.ValidationError('Password and Repeat Password must be the same')
'''
