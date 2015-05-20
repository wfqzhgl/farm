# -*-coding:utf-8-*-
'''
Created on 2015年5月7日

@author: faqingw
'''
from django.conf import settings
import json
import copy
import os
from models import *
import logging

logger = logging.getLogger(__name__)

def login_check(func):
    def render(request, *args, **kwargs):
        token = request.META.get(settings.VEG_SESSION_HEADER_KEY)
        if token and settings.REDIS_CLIENT.hexists(settings.HASHKEY_APPS_USER_TOKEN, token):
            return_data = func(request, *args, **kwargs)
            return return_data
        return dict(code=1, msg='login required.', value=[])

    return render

def log_out_token(token):
    if not settings.REDIS_CLIENT.hexists(settings.HASHKEY_APPS_USER_TOKEN, token):
        return
    settings.REDIS_CLIENT.hdel(settings.HASHKEY_APPS_USER_TOKEN, token)
    

def log_in_token(token, user_dict):
    if not settings.REDIS_CLIENT.hexists(settings.HASHKEY_APPS_USER_TOKEN, token):
        settings.REDIS_CLIENT.hset(settings.HASHKEY_APPS_USER_TOKEN, token, json.dumps(user_dict))

def get_userdict_from_token(request,header_name="HTTP_VEGSESSION"):
    token = request.META.get(header_name)
    if not token:
        return None
    u = settings.REDIS_CLIENT.hget(settings.HASHKEY_APPS_USER_TOKEN, token)
    try:
        return json.loads(u)
    except Exception,e:
        logger.error(str(e))
        return None
    

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
    if isinstance(Obj, FarmInfo):
        rs = PlantRecord.objects.filter(farm=Obj, finished=False)
        if rs:
            val['owner'] = get_dict_from_model(rs[0].owner)
            val['plant'] = get_dict_from_model(rs[0].plant)
        pics = []
        for pic in Obj.pics.all():
            pics.append(settings.MEDIA_URL + os.path.basename(pic.url))
        val['pics'] = pics
        
    return val
