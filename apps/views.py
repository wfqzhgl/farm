# -*-coding:utf8-*-

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from forms import *
from helper import *
import random
import os
import logging
from public.utils import render_to_json, gen_file_name, handle_uploaded_file

logger = logging.getLogger(__name__)

@csrf_exempt
@render_to_json
def reg(request):
    """注册"""
    fm = UserInfoForm(request.POST, initial={"balance": 0.0})
    code = 0
    msg = ''
    userinfo = None
    logger.debug('request.POST:%s' % request.POST)
    if fm.is_valid():
        userinfo = fm.save()
        userinfo = userinfo.__dict__
        del userinfo['created']
        del userinfo['_state']
        del userinfo['psw']
    else:
        code = 1
#         msg = '%s' % fm.errors.as_json()
        msg = '%s' % repr(fm.errors)
        
    return dict(code=code, msg=msg, value=[userinfo])

@csrf_exempt
@render_to_json
def login(request):
    """登录"""
    fm = LoginForm(request, request.POST)
    code = 0
    msg = 'OK'
    userinfo = None
    logger.debug('request.POST:%s' % request.POST)
    if fm.is_valid():
        userinfo = fm.get_user()
    else:
        code = 1
#         msg = '%s' % fm.errors.as_json()
        msg = '%s' % repr(fm.errors)
        
    return dict(code=code, msg=msg, value=[userinfo])

@csrf_exempt
@render_to_json
def logout(request):
    """注销
    VEG_SESSION
    """
    code = 0
    msg = 'OK'
    token = request.META.get('VEG_SESSION')
    try:
        log_out_token(token)
    except Exception, e:
        code = 1
        msg = e.message
    return dict(code=code, msg=msg, value=[])

@login_required
def get_user_info(request):
    """获取用户详细信息"""
    code = 0
    msg = 'OK'
    pass


@login_required
def modify_user_info(request):
    """个人信息修改"""
    code = 0
    msg = 'OK'
    pass

@csrf_exempt
@render_to_json
def rdm_user_info(request):
    """随机获取一个用户信息"""
    code = 0
    msg = 'OK'
    count = UserInfo.objects.count()
    userinfo = UserInfo.objects.all()[random.randint(0, count - 1)]
    userinfo = get_dict_from_model(userinfo)
    return dict(code=code, msg=msg, value=[userinfo])

@login_required
def get_time_line(request):
    """土地时间轴"""
    code = 0
    msg = 'OK'
    pass

@login_required
def get_farm_info(request):
    """获取土地详情"""
    code = 0
    msg = 'OK'
    pass

@login_required
def get_farm_list(request):
    """获取用户的土地列表"""
    code = 0
    msg = 'OK'
    pass

@login_required
def get_buddy_list(request):
    """获取用户好友列表"""
    code = 0
    msg = 'OK'
    pass

@login_required
def buddy_follow(request):
    """添加好友"""
    code = 0
    msg = 'OK'
    pass

@login_required
def get_free_farm_list(request):
    """获取尚未租种的土地列表"""
    code = 0
    msg = 'OK'
    pass

@login_required
def get_op_history(request):
    """获取操作记录"""
    code = 0
    msg = 'OK'
    pass

@login_required
def get_plant_for_farm(request):
    """获取土地可以播种的农作物列表"""
    code = 0
    msg = 'OK'
    pass

@login_required
def apply_for_farm(request):
    """土地具体操作"""
    code = 0
    msg = 'OK'
    pass

@login_required
def get_comments_of_timeline(request):
    """获取图片评论信息"""
    code = 0
    msg = 'OK'
    pass

@login_required
def edit_comment(request):
    """图片评论编辑"""
    code = 0
    msg = 'OK'
    pass


@login_required
def search(request):
    """土地，农作物搜索（暂略）"""
    code = 0
    msg = 'OK'
    pass


@login_required
def upload_time_line(request):
    """图片上传"""
    code = 0
    msg = 'OK'
    pass

@csrf_exempt
@render_to_json
def upload(request):
    fm = PicForm(request.POST, request.FILES)
    code = 0
    msg = ''
    url = ''
    logger.debug('request.FILES:%s' % request.FILES)
    if fm.is_valid():
        pic = fm.save()
        if 'file' in request.FILES:
            file1 = request.FILES.get('file')
            filename1 = gen_file_name(file1)  # 生成文件 
            handle_uploaded_file(os.path.join(settings.MEDIA_ROOT, filename1), file1)
            if filename1:
                saveurl = '/media/' + filename1
                pic.url = saveurl
                pic.save()
                url = os.path.join(settings.MEDIA_URL, filename1)
    else:
        code = 1
#         msg = '%s' % fm.errors.as_json()
        msg = '%s' % repr(fm.errors)
        
    return dict(code=code, msg=msg, value=[url])

@login_required
def modify_op(request):
    """操作记录修改"""
    pass

@login_required
def recharge(request):
    """充值"""
    pass
