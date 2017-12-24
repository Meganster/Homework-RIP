# coding=utf-8
from django import forms


class RegistrationForm(forms.Form):
    username = forms.CharField(min_length=5, label='Имя пользователя (логин)')
    email = forms.EmailField()
    firstname = forms.CharField(label='Имя')
    lastname = forms.CharField(label='Фамилия')
    password = forms.CharField(min_length=8, label='Пароль', widget=forms.PasswordInput)
    confirmpass = forms.CharField(min_length=8, label='Подтвердите пароль', widget=forms.PasswordInput)


class LoginForm(forms.Form):
    username_or_email = forms.CharField(label='Имя пользователя (эл. почта)')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)