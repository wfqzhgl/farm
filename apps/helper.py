# -*-coding:utf-8-*-
'''
Created on 2015年5月7日

@author: faqingw
'''
from django.conf import settings
import json
import copy

def log_out_token(token):
    if not settings.REDIS_CLIENT.hexists(settings.HASHKEY_APPS_USER_TOKEN, token):
        return
    settings.REDIS_CLIENT.hdel(settings.HASHKEY_APPS_USER_TOKEN, token)
    

def log_in_token(token, user_dict):
    if not settings.REDIS_CLIENT.hexists(settings.HASHKEY_APPS_USER_TOKEN, token):
        settings.REDIS_CLIENT.hset(settings.HASHKEY_APPS_USER_TOKEN, token, json.dumps(user_dict))


def get_dict_from_model(Obj):
    val = copy.copy(Obj.__dict__)
    del val['_state']
    if hasattr(Obj, 'created'):
        del val['created']
    if hasattr(Obj, 'psw'):
        del val['psw']
    
    if hasattr(Obj, 'comments'):
        comments = []
        for oo in Obj.comments.order_by('-created'):
            oo_dic = oo.__dict__
            del oo_dic['_state']
            comments.append(oo_dic)
        val['comments'] = comments
    return val
