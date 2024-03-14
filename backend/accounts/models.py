from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser
from django.db import models




class CustomUser(AbstractUser): # хз кароче прокладка чтобы можно было телефон указать 
    phone = models.CharField(max_length=20, blank=True, null=True)


class UserRegistrationForm(forms.ModelForm):
    email = forms.EmailField(label='Электронная почта', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(label='Телефонный номер', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = CustomUser
        fields = ('email', 'phone')

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError('Этот email уже зарегистрирован.')
        return email
        
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают.')
        return cd['password2']

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)

        user.email = self.cleaned_data['email']
        user.phone = self.cleaned_data['phone']
        user.username = user.email
        user.set_password(self.cleaned_data["password"])

        if commit:
            user.save()
        return user
