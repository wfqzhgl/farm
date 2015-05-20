# -*-coding:utf-8-*-
__author__ = 'wufaqing'

import re
import linecache
import sys
import urllib2
import os
import time
import uuid
import json
import decimal
import urllib
import smtplib
from email.mime.text import MIMEText
import logging
from datetime import date, timedelta, datetime
from django.conf import settings
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.db import connections, transaction
from django.http import HttpResponse

try:
    import hashlib
    hash_max = hashlib
except ImportError:
    import md5
    hash_max = md5

from xxtea import decrypt, encrypt


logger = logging.getLogger(__name__)

def render_to_json(func):
    def render(request, *args, **kwargs):
        return_data = func(request, *args, **kwargs)
        if isinstance(return_data, dict):
            data = json.dumps(return_data, cls=CJsonEncoder)
            return HttpResponse(data)
        else:
            return return_data

    return render

def gen_file_name(file):
    """
            获取文件name
    """
    if not file:
        return ''
    path = str(file)
    filename = os.path.splitext(path)[0]
    ext = os.path.splitext(path)[1]
    hash_name = hashlib.md5(filename).hexdigest()
    fn = time.strftime('%Y%m%d%H%M%S')
    return fn + '_' + hash_name + ext

def handle_uploaded_file(path, f):
    """
        upload file to specific path(include file name)
    """
    if not f:
        return
    destination = open(path, 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()
    
def md5_hex(s, len=32):
    """md5 hash
    """
    return hash_max.md5(s).hexdigest()[:len]


def get_real_ip(request):
    """生产环境有2层nginx代理，真实ip取HTTP_X_FORWARDED_FOR第一个非代理服务器（或内网）的外网ip.如：
        '219.236.246.147, 192.168.1.209'
        '10.81.50.139, 211.138.5.41, 192.168.1.209'

    """
    # #常用3类私有IP地址段
    local_ip_prefix = ['10.', '192.168.', '172.16.', '172.17.', '172.18.', '172.19.',
                       '172.20.', '172.21.', '172.22.', '172.23.', '172.24.', '172.25.',
                       '172.26.', '172.27.', '172.28.', '172.29.', '172.30.', '172.31.']
    ips = request.META.get('HTTP_X_FORWARDED_FOR', '')

    if not ips:
        ips = request.META.get('HTTP_X_REAL_IP', '-')
    list_ips = ips.split(',')
    ip = list_ips[0].strip()
    if len(list_ips) > 2:
        if ip.startswith(local_ip_prefix[0]) or ip.startswith(local_ip_prefix[1]):
            ip = list_ips[1].strip()
        elif ip.startswith('172.'):
            for ll in local_ip_prefix[2:]:
                if ip.startswith(ll):
                    ip = list_ips[1].strip()
                    break
                    # logger.info("X_FORWARDED_FOR=" + ips + "   X_REAL_IP=" + request.META.get('HTTP_X_REAL_IP', '-') + "   ip=" + ip)
    return ip


def get_location_from_ip(ip, use_local=False):
    if not ip:
        return None
    ip = ip.strip()
    return parse_ip_by_local(ip)



def parse_ip_by_local(ip):
    res = None
    try:
        geos = settings.IPPARSER.find(ip)
        if geos:
            # #国家 省 城市 单位
            geos = geos.strip()
            geos = re.split(r'\t', geos)[:3]
            if len(geos) == 2:  # 国家, 直辖市
                res = (geos[0], geos[1], geos[1], '')
            elif len(geos) == 3:
                geos.append('')
                res = geos
                if not res[2]:
                    res[2] = res[1]
            elif len(geos) == 1:
                res = (geos[0], geos[0], geos[0], '')
    except Exception, e:
        logger.error(str(e))
    return res


def encode_str(s, key):
    """
    >>> s = "hello"
    >>> key = "key"
    >>> encode_str(s, key)
    'e0ffbc367ebfbb420c61f2d90dd9ea15eeffede8fee0f643a5b3f2fe303feda6'
    """
    return encrypt(s, key)


def decode_str(enc, key):
    """
    >>> enc="e0ffbc367ebfbb420c61f2d90dd9ea15eeffede8fee0f643a5b3f2fe303feda6"
    >>> key="key"
    >>> decrypt(enc,key)
    u'hello'
    """
    return decrypt(enc, key)


def get_range_by_week(year, week):
    d = date(year, 1, 1)
    d = d - timedelta(d.weekday())
    dlt = timedelta(days=(week - 1) * 7)
    return d + dlt, d + dlt + timedelta(days=6)


def get_uuid():
    """获取唯一ID

    """
    return uuid.uuid4().hex


def get_page_obj(request, queryset, perpage=30, tag=None):
    """
            获取分页对象
            输入：request：request；queryset：分页对象数据；perpage：页码，默认为30
            输出：分页后的对象数据
    """
    if perpage == "all" or perpage == 0:
        perpage = len(queryset)
        perpage = perpage if perpage > 0 else 1
    else:
        try:
            perpage = int(perpage)
        except:
            perpage = 30

    p = Paginator(queryset, perpage)
    try:
        page = request.REQUEST.get('page', None)
        if not page:
            kk = ('f_page' + tag) if tag else 'f_page'
            page = request.COOKIES.get(kk, 1)
        page = int(page)
    except ValueError:
        page = 1
    try:
        page_obj = p.page(page)
    except (EmptyPage, InvalidPage):
        page_obj = p.page(p.num_pages)
    return page_obj


def run_query_sql(strSql, args=None):
    """
            直接运行sql语句
    """
    connection = connections['default']
    cursor = connection.cursor()
    if args:
        cursor.execute(strSql, args)
    else:
        cursor.execute(strSql)
#     transaction.commit_unless_managed()
    result_rows = cursor.fetchall()
    return result_rows


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)


def get_from_redis(key):
    try:
        return settings.REDIS_CLIENT.get(key)
    except Exception, e:
        logger.error(str(e))
        return None


def set_to_redis(key, val, expire=None):
    try:
        settings.REDIS_CLIENT.set(key, val, expire)
    except Exception, e:
        logger.error(str(e))
        return None


def save_to_redis_list(key, str_val):
    settings.REDIS_CLIENT.rpush(key, str_val)


#    logger.debug("save_to_redis_list: "+key+','+str_val)

def get_from_redis_list(key):
    str_val = settings.REDIS_CLIENT.lpop(key)
    #    logger.debug("get_redis_list: "+key+','+str(str_val))
    return str_val


def print_exception():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    return 'EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj)


def valid_phone_num(num):
    """
    >>> a = '13403044888'
    >>> b = '123123asdas'
    >>> c = ''
    >>> d = ' '
    >>> valid_phone_num(a)
    True
    >>> valid_phone_num(b)
    False
    >>> valid_phone_num(c)
    False
    >>> valid_phone_num(d)
    False

    """
    if not num or not num.strip():
        return False
    return True if re.match(r'^1[\d]{10}$', num.strip()) else False


def send_mail(to_list, sub, content,
              mail_host="smtp.163.com",
              mail_user="oupeng_reminder",
              mail_postfix="@163.com",
              mail_pass="oupengreminder"):
    '''
    mail_host = "smtp.163.com"
    mail_user = "oupeng_reminder"
    mail_postfix = "@163.com"
    mail_pass = "oupengreminder"
    '''
    logger.debug('----sending email to %s' % str(to_list))

    from_addr = mail_user + mail_postfix
    msg = MIMEText(content, _charset="utf-8")
    msg["Accept-Language"] = "zh-CN"
    msg["Accept-Charset"] = "ISO-8859-1,utf-8"
    msg['Subject'] = sub
    msg['From'] = from_addr
    msg['To'] = ";".join(to_list)
    # msg['Cc'] = ";".join(email_cc_list)
    try:
        s = smtplib.SMTP()
        s.connect(mail_host)
        s.login(mail_user, mail_pass)
        s.sendmail(from_addr, to_list, msg.as_string())
        s.close()
        logger.debug("--------ok sended email:" + str(to_list))
        return True
    except Exception, e:
        logger.error("--------error sending email:" + str(e))
        return False


class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)
        
        
if __name__ == "__main__":
    import doctest

    doctest.testmod()
    # print get_range_by_week(2014, 2)
    print decode_str('7500daa1ea1e1d8d177d110e49a844c168b7b0565c521173cc04aecac6becf40', 'OUPENG3609ec3c97c59')
    print decode_str('ac09996c311255fdfa83034933c1c61d4fdab60e9ab5887fc5cce626f9ce2824', 'OUPENG3609ec3c97c59')
