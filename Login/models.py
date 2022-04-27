import datetime

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django import forms
from django.forms.utils import ErrorList
from django.db import models

# Create your models here.
#
# class User(models.Model):
#     uid = models.AutoField(primary_key=True)
#     username = models.CharField(unique=True, max_length=30)
#     password = models.CharField(max_length=128)
#     email = models.CharField(max_length=32)
#     regtime = models.DateTimeField()
#     jurisdiction = models.IntegerField()
#     sex = models.IntegerField(blank=True, null=True)
#
#     class Meta:
#         # managed = False
#         db_table = 'user'
#
#     def __str__(self):
#         return self.username + str(self.uid)
#
# class UserTable():
#     def __init__(self):
#         pass
#
#     def inset(self, userinfo):
#         user = User()
#         user.username = userinfo.get('username')
#         user.password = userinfo.get('password')
#         user.email = userinfo.get('email')
#         user.jurisdiction = 0
#         user.regtime = str(datetime.date.today())
#         user.save()
#
#     def __str__(self):
#         pass


class User(AbstractUser):
    uid = models.AutoField(primary_key=True)
    username = models.CharField(unique=True, max_length=30)
    password = models.CharField(max_length=128)
    email = models.CharField(max_length=32)
    regtime = models.DateTimeField()
    jurisdiction = models.IntegerField()
    sex = models.IntegerField(blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'user'

class RegisterForm(forms.Form):
    # def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
    #              initial=None, error_class=ErrorList, label_suffix=None,
    #              empty_permitted=False, field_order=None, use_required_attribute=None, renderer=None,request=None):
    #     super().__init__(data,files,auto_id,prefix,label_suffix,empty_permitted,field_order,use_required_attribute,renderer)
    #     self.request = request

    username = forms.CharField(min_length=3,required=True,error_messages={
        'required':'用户名必须输入',
        'min_length':'用户名至少3个字符'
    })
    password = forms.CharField(min_length=3,required=True,error_messages={
        'required': '密码名必须输入',
        'min_length': '密码至少3个字符'
    })
    confirm = forms.CharField(min_length=3,required=True,error_messages={
        'required': '密码名必须输入',
        'min_length': '密码至少3个字符'
    })

    # 单个字段验证: clean_xxxx
    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password and password.isdigit():
            raise ValidationError("密码不能是纯数字")
        return password

    # 全局验证
    def clean(self):
        password = self.cleaned_data.get('password',None)
        confirm = self.cleaned_data.get('confirm','')
        print(password,confirm)
        if password != confirm:
            raise ValidationError({'confirm':"两次密码输入不一致"})
        return self.cleaned_data
