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


def get_dict_from_model(userinfo):
    val = copy.copy(userinfo.__dict__)
    del val['_state']
    if hasattr(userinfo, 'created'):
        del val['created']
    if hasattr(userinfo, 'psw'):
        del val['psw']
    return val
