# -*-coding:utf8-*-

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from forms import *
from helper import *
import random
import os
from datetime import datetime
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
@login_check
def logout(request):
    """注销
    """
    code = 0
    msg = 'OK'
    token = request.META.get(settings.VEG_SESSION_HEADER_KEY)
    try:
        log_out_token(token)
    except Exception, e:
        code = 1
        msg = e.message
    return dict(code=code, msg=msg, value=[])


@csrf_exempt
@render_to_json
@login_check
def change_psw(request):
    code = 0
    msg = 'OK'
    psw_old = request.REQUEST.get('psw_old')
    psw_new_1 = request.REQUEST.get('psw_new_1')
    psw_new_2 = request.REQUEST.get('psw_new_2')
    userdict = get_userdict_from_token(request)
    users = UserInfo.objects.filter(id=userdict['id'])
    if psw_new_1 != psw_new_2:
        return dict(code=1, msg='new psw not equls.', value=[])
    if not users:
        return dict(code=1, msg='user not exists.', value=[])
    if users[0].psw != psw_old:
        return dict(code=1, msg='psw_old error.', value=[])
    users[0].psw = psw_new_1
    users[0].save()
    return dict(code=code, msg=msg, value=[get_dict_from_model(users[0])])
    

@csrf_exempt
@render_to_json
@login_check
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
@login_check
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
@login_check
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
# @login_check
def get_time_line(request):
    """土地时间轴"""
    code = 0
    msg = 'OK'
#     uid = request.REQUEST.get('uid')
    fid = request.REQUEST.get('fid')
    page = request.REQUEST.get('page', 0)
    farms = FarmInfo.objects.filter(id=fid)
    if  not fid or not farms:
        return dict(code=1, msg='error', value=[])
#     prs = PlantRecord.objects.filter(owner__uid=uid, farm__id=fid, finished=False)
    prs = PlantRecord.objects.filter(rentrecord__farm__id=fid, finished=False)
    if not prs:
        return dict(code=0, msg='no timeline', value=[[], [], get_dict_from_model(farms[0])])
    prs = prs[0]
    tls = TimelineInfo.objects.filter(plantrecord=prs).order_by('-date')
    objs = get_page_obj(request, tls, settings.ROWS_DEFAULT)
    res = [get_dict_from_model(obj) for obj in objs]
    havest = [] if not prs.havest else prs.havest.split(',')
    return dict(code=code, msg=msg, value=[res, havest, get_dict_from_model(farms[0])])


@csrf_exempt
@render_to_json
@login_check
def pic_praise(request):
    """
        参数： 
        tid     timeline id
        fid 土地id
    """
    code = 0
    msg = 'OK'
    tid = request.REQUEST.get('tid')
    fid = request.REQUEST.get('fid')
    tls = TimelineInfo.objects.filter(id=tid)
    if not tls:
        return dict(code=1, msg='no timeline.', value=[])
    tls[0].admire = tls[0].admire + 1
    tls[0].save()
    return dict(code=code, msg=msg, value=[])

@csrf_exempt
@render_to_json
@login_check
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
# @login_check
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
        for pr in RentRecord.objects.filter(owner__uid=uid, finished=False).order_by('-created'):
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
            if tl.plantrecord.rentrecord.farm not in farmlist:
                farmlist.append(tl.plantrecord.rentrecord.farm)
            if len(farmlist) >= 4:
                break
        if not farmlist:
            prs = PlantRecord.objects.filter(finished=False).order_by('-id')
            if prs:
                farmlist.append(prs[0].rentrecord.farm)
        farm_admire = [get_dict_from_model(obj) for obj in farmlist]
    return dict(code=code, msg=msg, value=[farm_self, farm_admire, farm_rdm])

@csrf_exempt
@render_to_json
@login_check
def get_buddy_list(request):
    """获取用户好友列表"""
    code = 0
    msg = 'OK'
    uid = request.REQUEST.get('uid')
    userdict = get_userdict_from_token(request)
    thisuid = uid if uid else userdict['uid']
    users = UserInfo.objects.filter(uid=thisuid)
    if not users:
        return dict(code=1, msg='user not exists.', value=[])
    res = [get_dict_from_model(obj) for obj in users[0].buddys.all()]
    return dict(code=code, msg=msg, value=res)

@csrf_exempt
@render_to_json
@login_check
def buddy_follow(request):
    """添加好友
        uid      // 需要follow的uid，本身uid通过session获取
        follow // true, 加好友， false 取消关注
    """
    code = 0
    msg = 'OK'
    uid = request.REQUEST.get('uid')
    follow = request.REQUEST.get('follow')
    userdict = get_userdict_from_token(request)
    user = UserInfo.objects.get(id=userdict['id'])
    buddys = UserInfo.objects.filter(uid=uid)
    if uid == userdict['uid'] or not buddys:
        return dict(code=1, msg='uid error', value=[])
    if follow == 'true':
        user.buddys.add(buddys[0])
    elif follow == 'false':
        user.buddys.remove(buddys[0])
    else:
        return dict(code=1, msg='follow error', value=[])
    return dict(code=code, msg=msg, value=[])

@csrf_exempt
@render_to_json
@login_check
def get_free_farm_list(request):
    """获取尚未租种的土地列表"""
    code = 0
    msg = 'OK'
    fids = RentRecord.objects.filter(finished=False).values_list('farm_id', flat=True)
    fis = FarmInfo.objects.exclude(id__in=fids)
    objs = get_page_obj(request, fis, settings.ROWS_DEFAULT)
    farm_list = [get_dict_from_model(obj) for obj in objs]
    return dict(code=code, msg=msg, value=farm_list)

@csrf_exempt
@render_to_json
@login_check
def get_op_history(request):
    """获取操作记录"""
    code = 0
    msg = 'OK'
    userdict = get_userdict_from_token(request)
    ops = OperationInfo.objects.filter(operator_id=userdict['id']).order_by('-created')
    objs = get_page_obj(request, ops, settings.ROWS_DEFAULT)
    return dict(code=code, msg=msg, value=[get_dict_from_model(obj) for obj in objs])

@csrf_exempt
@render_to_json
@login_check
def get_comsume_history(request):
    code = 0
    msg = 'OK'
    userdict = get_userdict_from_token(request)
    ops = ConsumeRecord.objects.filter(user_id=userdict['id']).order_by('-created')
    objs = get_page_obj(request, ops, settings.ROWS_DEFAULT)
    return dict(code=code, msg=msg, value=[get_dict_from_model(obj) for obj in objs]) 

@csrf_exempt
@render_to_json
@login_check
def get_plant_for_farm(request):
    """获取土地可以播种的农作物列表"""
    code = 0
    msg = 'OK'
    plants = []
    fid = request.REQUEST.get('fid')
    if not fid:
        return dict(code=1, msg='no fid', value=[])
    try:
        farm = FarmInfo.objects.get(id=fid)
        for plt in farm.plants.all():
            plants.append(get_dict_from_model(plt))
        if not plants:
            for plt in PlantInfo.objects.all():
                plants.append(get_dict_from_model(plt))
    except Exception, e:
        code = 1
        return dict(code=1, msg='fid error', value=[])
    return dict(code=code, msg=msg, value=plants)


@csrf_exempt
@render_to_json
@login_check
def unrent_for_farm(request):
    """unrent
    """
    code = 0
    msg = 'OK'
    fid = request.REQUEST.get('fid')
    if not fid:
        return dict(code=1, msg='no fid error', value=[])
    userdict = get_userdict_from_token(request)
    rrs = RentRecord.objects.filter(farm_id=fid, owner_id=userdict['id'], finished=False)
    if not rrs:
        return dict(code=1, msg='The farm not owned.', value=[])
    today = datetime.now().date()
    rrs[0].finished = True
    rrs[0].end = today
    rrs[0].save()
    return dict(code=code, msg=msg, value=[])

    
@csrf_exempt
@render_to_json
@login_check
def rent_for_farm(request):
    """租用土地
    """
    code = 0
    msg = 'OK'
    fid = request.REQUEST.get('fid')
    if not fid:
        return dict(code=1, msg='no fid error', value=[])
    userdict = get_userdict_from_token(request)
    rrs = RentRecord.objects.filter(farm_id=fid, finished=False)
    if rrs:
        return dict(code=1, msg='The farm not free.', value=[])
    today = datetime.now().date()
    rr = RentRecord(owner_id=userdict['id'], farm_id=fid, begin=today)
    rr.save()
    return dict(code=code, msg=msg, value=[])


@csrf_exempt
@render_to_json
@login_check
def apply_for_farm(request):
    """土地具体操作
        fid     farm id
        type    操作类型: PLANT, WEED, WATERING, DEBUG, PICK, REMOVE, OTHER
        appdix     不同操作类型所需不同参数
        PLANT 时需要参数；appdix 的值为plant id
    """
    code = 0
    msg = 'OK'
    fid = request.REQUEST.get('fid')
    type = request.REQUEST.get('type')
    appdix = request.REQUEST.get('appdix')
    
    # get cost
    consume = 0.0
    ocs = OperationCost.objects.filter(type=type)
    if ocs:
        consume = ocs[0].consume
    userdict = get_userdict_from_token(request)
    try:
        userinfo = UserInfo.objects.get(uid=userdict['uid'])
    except Exception, e:
        code = 1
        return dict(code=1, msg='no user error', value=[])
    today = datetime.now().date()
    plantrecord = None
    if type == 'PLANT':
        plant_id = appdix
        rrs = RentRecord.objects.filter(owner_id=userdict['id'], farm_id=fid, finished=False)
        if not rrs:
            return dict(code=1, msg='The farm not yours.', value=[])
        prs = PlantRecord.objects.filter(rentrecord__farm__id=fid, finished=False)
        if prs:
            if prs[0].plant:
                return dict(code=1, msg='The farm not free.', value=[])
            else:
                prs[0].plant_id = plant_id
                prs[0].save()
                
        else:
            plantrecord = PlantRecord(rentrecord=rrs[0], plant_id=plant_id, begin=today)
            plantrecord.save()
    elif type == 'REMOVE':
        prs = PlantRecord.objects.filter(rentrecord__farm__id=fid, finished=False)
        prs.update(finished=True)
    op = OperationInfo(farm_id=fid, plantrecord=plantrecord, name=type, type=type,
                       date=today, operator_id=userdict['id'], consume=consume)
    op.save()
    # add consume record
    cr = ConsumeRecord(user_id=userdict['id'], type=type, cid=op.id, consume=consume)
    cr.save()
    
    # subtract consume
    if consume > 0.0:
        userinfo.balance = userinfo.balance - consume;
        userinfo.save()
    return dict(code=code, msg=msg, value=[])

@csrf_exempt
@render_to_json
@login_check
def get_comments_of_timeline(request):
    """获取图片评论信息"""
    code = 0
    msg = 'OK'
    tid = request.REQUEST.get('tid')
    if not tid:
        return dict(code=1, msg='no tid', value=[])
    tis = TimelineInfo.objects.filter(id=tid)
    if not tis:
        return dict(code=1, msg='tid error.', value=[])
    res = [get_dict_from_model(obj) for obj in tis[0].comments.all()]
    return dict(code=code, msg=msg, value=res)

@csrf_exempt
@render_to_json
@login_check
def edit_comment(request):
    """图片评论编辑
        tid     timeline id
        type 操作类型：DEL, ADD, EDIT
        cid comment id
        mes 操作所需参数，如DEL则不需参数
    """
    code = 0
    msg = 'OK'
    tid = request.REQUEST.get('tid')
    ctype = request.REQUEST.get('type')
    mes = request.REQUEST.get('mes')
    cid = request.REQUEST.get('cid')
    if not type or not tid:
        return dict(code=1, msg='para error.', value=[])
    udict = get_userdict_from_token(request)
    if ctype == 'ADD':
        co = Comment(user_id=udict['id'], desc=mes)
        co.save()
        ti = TimelineInfo.objects.get(id=tid)
        ti.comments.add(co)
    elif ctype == 'EDIT':
        cos = Comment.objects.filter(id=cid)
        if cos:
            cos[0].desc = mes
            cos[0].save()
    elif ctype == 'DEL':
        cos = Comment.objects.filter(id=cid)
        if cos:
            cos[0].deleted = True
            cos[0].save()
    return dict(code=code, msg=msg, value=[])


@csrf_exempt
@render_to_json
@login_check
def search(request):
    """土地，农作物搜索（暂略）"""
    code = 0
    msg = 'OK'
    pass


@csrf_exempt
@render_to_json
@login_check
def upload_time_line(request):
    """图片上传
        fid 此图片对应的farm id
        pic
        msg 针对图片的描述
    """
    code = 0
    msg = 'OK'
    fid = request.REQUEST.get('fid')
    pic = request.REQUEST.get('pic')
    appendix = request.REQUEST.get('msg')
    udict = get_userdict_from_token(request)
    today = datetime.now().date()
    prs = PlantRecord.objects.filter(rentrecord__farm__id=fid, finished=False)
    if not prs:
        return dict(code=1, msg='no plantrecord.', value=[])
    tl = TimelineInfo(plantrecord=prs[0], pic=pic, date=today,
                      poster_id=udict['id'], appendix=appendix)
    tl.save()
    return dict(code=code, msg=msg, value=[])
    

@csrf_exempt
@render_to_json
# @login_check
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
@login_check
def modify_op(request):
    """操作记录修改"""
    pass

@csrf_exempt
@render_to_json
@login_check
def recharge(request):
    """充值"""
    code = 0
    msg = 'OK'
    uid = request.REQUEST.get('uid')
    charge = request.REQUEST.get('charge')
    
    ccs = ChargeCard.objects.filter(num=charge, invalid=False)
    if not ccs:
        return dict(code=1, msg='card error.', value=[])
    us = UserInfo.objects.filter(uid=uid)
    if not us:
        return dict(code=1, msg='uid error.', value=[])
    # update user
    us[0].balance = (us[0].balance if us[0].balance else 0) + ccs[0].count
    us[0].save()
    # update card
    ccs[0].invalid = True
    ccs[0].save()
    # add history
    ch = ChargeHistory(uid=uid, num=charge)
    ch.save()
    # add consume record
    cr = ConsumeRecord(user_id=us[0].id, type='RECHARGE', cid=ch.id, consume=ccs[0].count)
    cr.save()
    return dict(code=code, msg=msg, value=[get_dict_from_model(us[0])])
    
