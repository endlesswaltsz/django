from django import forms
from django.forms import widgets
from django.core.exceptions import ValidationError
from blog import models


class UserForm(forms.Form):
    username = forms.CharField(label='用户名',widget=widgets.TextInput(attrs={'class': 'form-control'}), max_length=8, min_length=5,
                               error_messages={
                                   'min_length': '用户名至少5位！',
                                   'max_length': '用户名最多8位！',
                                   'required': '该字段必填！'
                               })
    email = forms.EmailField(label='邮箱',widget=widgets.EmailInput(attrs={'class': 'form-control'}), error_messages={
        'invalid': '邮箱格式不合法！',
        'required': '该字段必填！'
    })
    password = forms.CharField(label='密码',max_length=16, min_length=5,
                               widget=widgets.PasswordInput(attrs={'class': 'form-control'}),
                               error_messages={
                                   'min_length': '密码至少5位！',
                                   'max_length': '密码最16位！',
                                   'required': '该字段必填！'
                               })
    re_password = forms.CharField(label='确认密码',widget=widgets.PasswordInput(attrs={'class': 'form-control'}),
                                  error_messages={'required': '该字段必填！'})

    def clean_username(self):
        username = self.cleaned_data.get('username')
        user = models.UserInfo.objects.filter(username=username)
        if not user:
            return username
        raise ValidationError('该用户名已存在！')

    # def clean_password(self):
    #     password = self.cleaned_data.get('password')
    #     if password[0].isalpha():
    #         return password
    #     raise ValidationError('密码必须以字母开头！')

    def clean(self):
        password = self.cleaned_data.get('password')
        re_password = self.cleaned_data.get('re_password')
        if password == re_password:
            return self.cleaned_data
        raise ValidationError('两次密码输入不一致!')
