# -*-coding:utf8-*-
'''
Created on 2015年5月4日

@author: faqingw
'''

from django.forms import ModelForm
from django.forms.util import ErrorList
from django import forms
from django.utils.translation import ugettext, ugettext_lazy as _
from django.conf import settings
import copy
import json
from  models import *
from public.utils import md5_hex
import time


class PicForm(ModelForm):
    class Meta:
        model = Pic
        fields = '__all__'
        
        
class UserInfoForm(ModelForm):
    class Meta:
        model = UserInfo
        fields = '__all__'
#     def clean_balance(self):
#         data = self.cleaned_data.get('balance', 0.0)
#         return data
        
    def clean_name(self):
        data = self.cleaned_data['name']
#         if "fred@example.com" not in data:
#             raise forms.ValidationError("name error!")

        # Always return the cleaned data, whether you have changed it or
        # not.
        return data
#     def clean(self):
#         # Don't allow draft entries to have a pub_date.
#         if self.status == 'draft' and self.pub_date is not None:
#             raise ValidationError('Draft entries may not have a publication date.')

class LoginForm(forms.Form):
    """
    """
    uid = forms.CharField(max_length=254)
    psw = forms.CharField(label=_("Password"), widget=forms.PasswordInput)
    def __init__(self, request=None, *args, **kwargs):
        """
        """
        self.request = request
        self.user_cache = None
        self.token = None
        super(LoginForm, self).__init__(*args, **kwargs)
    def clean(self):
        uid = self.cleaned_data.get('uid')
        psw = self.cleaned_data.get('psw')

        if uid and psw:
            self.user_cache = authenticate(uid=uid,
                                           psw=psw)
            if self.user_cache is None:
                raise forms.ValidationError(
                    'invalid_login',
                    code='invalid_login'
                )
        return self.cleaned_dat
    def get_user(self):
        return self.user_cache
    
    
def authenticate(uid, psw):
    user = UserInfo.objects.filter(uid=uid)
    if not user:
        return None
    user = user[0]
    if user.psw != psw:
        return None
    return get_token_and_user(user)

def get_token_and_user(user):
    token = md5_hex('%s%s' % (user.uid, time.time()))
    # update redis
    val = copy.copy(user.__dict__)
    del val['_state']
    del val['created']
    del val['psw']
    val['token'] = token
    print 'val=', val
    if not settings.REDIS_CLIENT.hexists(settings.HASHKEY_APPS_USER_TOKEN, token):
        settings.REDIS_CLIENT.hset(settings.HASHKEY_APPS_USER_TOKEN, token, json.dumps(val))
    return val
    
    
    
    
