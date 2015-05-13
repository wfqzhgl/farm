# -*-coding:utf8-*-

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from forms import *
from helper import *
import random
import os
import logging
from public.utils import render_to_json, gen_file_name, handle_uploaded_file, get_page_obj

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

@csrf_exempt
@render_to_json
def get_user_info(request):
    """获取用户详细信息"""
    code = 0
    msg = 'OK'
    uid = request.REQUEST.get('uid')
    if not uid:
        return dict(code=1, msg='no uid', value=[])
    try:
        userinfo = UserInfo.objects.get(uid=uid)
        userinfo = get_dict_from_model(userinfo)
    except Exception, e:
        code = 1
        return dict(code=1, msg='uid error', value=[])
    return dict(code=code, msg=msg, value=[userinfo])


@csrf_exempt
@render_to_json
def modify_user_info(request):
    """个人信息修改"""
    code = 0
    msg = 'OK'
    uid = request.REQUEST.get('uid')
    try:
        userinfo = UserInfo.objects.get(uid=uid)
    except Exception, e:
        code = 1
        return dict(code=1, msg='uid error', value=[])
#     print request.POST 
    for k, v in request.POST.items():
        if hasattr(userinfo, k) and v:
            setattr(userinfo, k, v)
    userinfo.save()
    return dict(code=code, msg=msg, value=[get_dict_from_model(userinfo)])

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

@csrf_exempt
@render_to_json
def get_time_line(request):
    """土地时间轴"""
    code = 0
    msg = 'OK'
    uid = request.REQUEST.get('uid')
    fid = request.REQUEST.get('fid')
    page = request.REQUEST.get('page', 0)
    if not uid or not fid:
        return dict(code=1, msg='error', value=[])
    prs = PlantRecord.objects.filter(owner__uid=uid, farm__id=fid, finished=False)
    if not prs:
        return dict(code=1, msg='no timeline', value=[])
    prs = prs[0]
    tls = TimelineInfo.objects.filter(plantrecord=prs).order_by('-created')
    objs = get_page_obj(request, tls, settings.ROWS_DEFAULT)
    res = [get_dict_from_model(obj) for obj in objs]
    havest = [] if not prs.havest else prs.havest.split(',')
    return dict(code=code, msg=msg, value=[res, havest])

@csrf_exempt
@render_to_json
def get_farm_info(request):
    """获取土地详情"""
    code = 0
    msg = 'OK'
    fid = request.REQUEST.get('fid')
    pic_count = request.REQUEST.get('pic_count')
    if not fid:
        return dict(code=1, msg='no fid', value=[])
    try:
        farm = FarmInfo.objects.get(id=fid)
        farm = get_dict_from_model(farm)
    except Exception, e:
        code = 1
        return dict(code=1, msg='fid error', value=[])
    return dict(code=code, msg=msg, value=[farm])

@csrf_exempt
@render_to_json
def get_farm_list(request):
    """获取用户的土地列表"""
    code = 0
    msg = 'OK'
    uid = request.REQUEST.get('uid')
    others = request.REQUEST.get('others')
    farm_self = []
    farm_admire = []
    farm_rdm = []
    if uid:
        farmlist = []
        for pr in PlantRecord.objects.filter(owner__uid=uid).order_by('-created'):
            if pr.farm not in farmlist:
                farmlist.append(pr.farm)
        if farmlist:
            farm_self = [get_dict_from_model(obj) for obj in farmlist]
    if others is not None:
        # radom
        fcount = FarmInfo.objects.count()
        farmlist = []
        if fcount <= 6:
            for farm in FarmInfo.objects.all():
                if farm not in farmlist:
                    farmlist.append(farm)
        else:
            baseindex = random.randint(0, fcount - 7)
            for i in xrange(6):
                farmlist.append(FarmInfo.objects.all()[baseindex + i])
        farm_rdm = [get_dict_from_model(obj) for obj in farmlist]
        # admire
        farmlist = []
        for tl in TimelineInfo.objects.order_by('-admire'):
            if tl.plantrecord.farm not in farmlist:
                farmlist.append(tl.plantrecord.farm)
            if len(farmlist) >= 4:
                break
        farm_admire = [get_dict_from_model(obj) for obj in farmlist]
    return dict(code=code, msg=msg, value=[farm_self, farm_admire, farm_rdm])

@csrf_exempt
@render_to_json
def get_buddy_list(request):
    """获取用户好友列表"""
    code = 0
    msg = 'OK'
    pass

@csrf_exempt
@render_to_json
def buddy_follow(request):
    """添加好友"""
    code = 0
    msg = 'OK'
    pass

@csrf_exempt
@render_to_json
def get_free_farm_list(request):
    """获取尚未租种的土地列表"""
    code = 0
    msg = 'OK'
    fids = PlantRecord.objects.filter(finished=False).values_list('farm_id', flat=True)
    fis = FarmInfo.objects.exclude(id__in=fids)
    farm_list = [get_dict_from_model(obj) for obj in fis]
    return dict(code=code, msg=msg, value=farm_list)

@csrf_exempt
@render_to_json
def get_op_history(request):
    """获取操作记录"""
    code = 0
    msg = 'OK'
    pass

@csrf_exempt
@render_to_json
def get_plant_for_farm(request):
    """获取土地可以播种的农作物列表"""
    code = 0
    msg = 'OK'
    pass

@csrf_exempt
@render_to_json
def apply_for_farm(request):
    """土地具体操作"""
    code = 0
    msg = 'OK'
    pass

@csrf_exempt
@render_to_json
def get_comments_of_timeline(request):
    """获取图片评论信息"""
    code = 0
    msg = 'OK'
    pass

@csrf_exempt
@render_to_json
def edit_comment(request):
    """图片评论编辑"""
    code = 0
    msg = 'OK'
    pass


@csrf_exempt
@render_to_json
def search(request):
    """土地，农作物搜索（暂略）"""
    code = 0
    msg = 'OK'
    pass


@csrf_exempt
@render_to_json
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

@csrf_exempt
@render_to_json
def modify_op(request):
    """操作记录修改"""
    pass

@csrf_exempt
@render_to_json
def recharge(request):
    """充值"""
    pass
