# -*-coding:utf8-*-
'''
Created on 2015年5月4日

@author: pure
'''

from django.forms import ModelForm
from django.forms.util import ErrorList
from django import forms
from django.utils.translation import ugettext, ugettext_lazy as _
from django.conf import settings
import copy
import json
from  models import *
from helper import *
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

class LoginForm(ModelForm):
    """
    """
    class Meta:
        model = LoginInfo
        fields = '__all__'
    def __init__(self, request=None, *args, **kwargs):
        """
        """
        self.request = request
        self.user_cache = None
        self.token = None
        super(LoginForm, self).__init__(*args, **kwargs)
    def clean(self):
        ltype = self.cleaned_data.get('type')
        uid = self.cleaned_data.get('uid')
        psw = self.cleaned_data.get('psw')
        #
        name = self.cleaned_data.get('name')
        email = self.cleaned_data.get('email')
        gender = self.cleaned_data.get('gender')
        portrait = self.cleaned_data.get('portrait')
        self_desc = self.cleaned_data.get('self_desc')
        appendix = self.cleaned_data.get('appendix')
        third_token = self.cleaned_data.get('third_token')
        third_id = self.cleaned_data.get('third_id')
        third_u_info = self.cleaned_data.get('third_u_info')

        if (ltype == 'GEN' and uid and psw) or (ltype != 'GEN' and third_id):
            self.user_cache = authenticate(ltype, uid, psw,
                                           name=name,
                                           gender=gender,
                                           email=email,
                                           portrait=portrait,
                                           self_desc=self_desc,
                                           appendix=appendix,
                                           third_token=third_token,
                                           third_id=third_id,
                                           third_u_info=third_u_info)
            if self.user_cache is None:
                raise forms.ValidationError(
                    'invalid_login',
                    code='invalid_login'
                )
        else:
            raise forms.ValidationError(
                    'invalid_login',
                    code='invalid_login'
                )
        return self.cleaned_data
    def get_user(self):
        return self.user_cache
    
    
def authenticate(ltype, uid, psw, **kargs):
    if ltype == 'GEN':
        user = UserInfo.objects.filter(type=ltype, uid=uid)
        if not user:
            return None
        user = user[0]
        if user.psw != psw:
            return None
    else:
        third_id = kargs.get('third_id')
        if not third_id:
            return None
        user = UserInfo.objects.filter(type=ltype, third_id=third_id)
        if user:
            user = user[0]
            # update
            for k, v in kargs.items():
                if hasattr(user, k) and v:
                    setattr(user, k, v)
            user.save()
        else:
            # add to userinfo
            new_uid = '%s-%s' % (ltype, third_id)
            new_psw = '123456'
            user = UserInfo(type=ltype, uid=new_uid, psw=new_psw, **kargs)
            user.save()
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
    log_in_token(token,val)
    return val
    
    
    
    
