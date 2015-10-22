# coding: utf-8
from django import forms


class RegisterForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm', widget=forms.PasswordInput)

    def pwd_validate(self, p1, p2):
        return p1 == p2


class LoginForm(forms.Form):
    username = forms.CharField(label=u'帐号')
    password = forms.CharField(label=u'密码', widget=forms.PasswordInput)
