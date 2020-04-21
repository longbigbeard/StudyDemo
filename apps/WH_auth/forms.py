
from django import forms
from apps.forms import FormMixin
from django.core.cache import cache
from .models import User


class LoginForm(forms.Form, FormMixin):
    telephone = forms.CharField(max_length=11)
    password = forms.CharField(max_length=10, min_length=6, error_messages={
        'max_length': "密码最长不超过10个字符", 'min_length': "密码最短不少于6个字符"
    })
    remember = forms.IntegerField(required=False)


class RegisterForm(forms.Form, FormMixin):

    telephone = forms.CharField(max_length=11)
    username = forms.CharField(max_length=20)
    password1 = forms.CharField(max_length=10, min_length=6, error_messages={
        'max_length': "密码最长不超过10个字符", 'min_length': "密码最短不少于6个字符"
    })
    password2 = forms.CharField(max_length=10, min_length=6, error_messages={
        'max_length': "密码最长不超过10个字符", 'min_length': "密码最短不少于6个字符"
    })
    img_captcha = forms.CharField(min_length=4, max_length=4)
    print(telephone,username,password1,password2,img_captcha)

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        telephone = cleaned_data.get('telephone')
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 != password2:
            raise forms.ValidationError("两次输入的密码不一致！")

        img_captcha = cleaned_data.get('img_captcha')
        cached_img_captcha = cache.get(img_captcha.lower())

        if not cached_img_captcha or cached_img_captcha.lower() != img_captcha.lower():
            raise forms.ValidationError("图形验证码错误！")

        exists = User.objects.filter(telephone=telephone).exists()
        if exists:
            forms.ValidationError("该手机号码已经被注册！")

        return cleaned_data


class EditPasswordForm(forms.Form,FormMixin):
    author_name = forms.CharField(max_length=20)
    author_passwd = forms.CharField(max_length=10,min_length=6)

