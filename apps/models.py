# -*-coding:utf8-*-


from django.db import models
import uuid


class LoginInfo(models.Model):
    TYPE_CHOICES = (
        ('GEN', u'GEN'),
        ('WEIBO', u'WEIBO'),
        ('QQ', u'QQ'),
        ('WEIXIN', u'WEIXIN'),
    )
    type = models.CharField("type", choices=TYPE_CHOICES, max_length=64, default='GEN')
    name = models.CharField("昵称", max_length=64, default='', blank=True, null=True)
    gender = models.CharField("性别", max_length=32, default='UNKNOWN')
    email = models.EmailField('email', blank=True, null=True)
    uid = models.CharField("username", max_length=64, blank=True, null=True)
    psw = models.CharField("passwd", max_length=64, blank=True, null=True)
    portrait = models.CharField("pic", max_length=256, blank=True, null=True)
    self_desc = models.CharField("self_desc", max_length=128, blank=True, null=True)
    appendix = models.CharField("appendix", max_length=128, blank=True, null=True)
    third_token = models.TextField("third_token", blank=True, null=True)
    third_id = models.CharField("third_id", max_length=128, blank=True, null=True)
    third_u_info = models.CharField("third_u_info", max_length=128, blank=True, null=True)
    created = models.DateTimeField("创建时间", auto_now_add=True)

class UserInfo(models.Model):
    TYPE_CHOICES = (
        ('GEN', u'GEN'),
        ('WEIBO', u'WEIBO'),
        ('QQ', u'QQ'),
        ('WEIXIN', u'WEIXIN'),
    )
    GENDER_CHOICES = (
        ('MALE', u'男'),
        ('FEMALE', u'女'),
        ('UNKNOWN', u'未知')
    )
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField("昵称", max_length=64, default='', blank=True, null=True)
    uid = models.CharField("username", max_length=64, unique=True)
    gender = models.CharField("性别", choices=GENDER_CHOICES, max_length=32, default='UNKNOWN')
    type = models.CharField("type", choices=TYPE_CHOICES, max_length=64, default='GEN')
    portrait = models.CharField("pic", max_length=256, blank=True, null=True)
#     portrait = models.FileField("头像", upload_to='.', help_text='', blank=True, null=True)
#     portrait_url = models.CharField("头像url", max_length=256, blank=True, null=True)
    email = models.EmailField('email', blank=True, null=True)
    psw = models.CharField("passwd", max_length=64)
    tel = models.CharField("tel", max_length=64, blank=True, null=True)
    addr = models.CharField("addr", max_length=128, blank=True, null=True)
#     token = models.CharField("token", max_length=64, blank=True, null=True)
    third_token = models.TextField("third_token", blank=True, null=True)
    third_id = models.CharField("third_id", max_length=128, blank=True, null=True)
    third_u_info = models.CharField("third_u_info", max_length=128, blank=True, null=True)
    self_desc = models.CharField("self_desc", max_length=128, blank=True, null=True)
    appendix = models.CharField("appendix", max_length=64, blank=True, null=True)
    balance = models.FloatField("balance", default=0.0, blank=True, null=True)
    created = models.DateTimeField("创建时间", auto_now_add=True)
    class Meta:
#         unique_together = (("brand", "province"),)
        verbose_name = "UserInfo"
        verbose_name_plural = "UserInfo MAG"
        
        
class OperationInfo(models.Model):
    """PLANT, WEED, WATERING, DEBUG, PICK, EMOVE, OTHER
    """
    OP_CHOICES = (
        ('PLANT', u'PLANT'),
        ('WEED', u'WEED'),
        ('WATERING', u'WATERING'),
        ('DEBUG', u'DEBUG'),
        ('PICK', u'PICK'),
        ('REMOVE', u'REMOVE'),
        ('OTHER', u'OTHER'),
    )
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    farm = models.ForeignKey("FarmInfo", verbose_name="FarmInfo id", blank=True, null=True)
    plantrecord = models.ForeignKey("PlantRecord", verbose_name="PlantRecord id", blank=True, null=True)
    name = models.CharField("name", max_length=64)
    type = models.CharField("type", choices=OP_CHOICES, max_length=32)
    date = models.DateTimeField("date")
    operator = models.ForeignKey("UserInfo", verbose_name="operator_id", blank=True, null=True)
    consume = models.FloatField("consume")
    created = models.DateTimeField("创建时间", auto_now_add=True)
    class Meta:
#         unique_together = (("brand", "province"),)
        verbose_name = "OperationInfo"
        verbose_name_plural = "OperationInfo MAG"
        
        
class PlantInfo(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField("name", max_length=64)
    output_of_per_unit = models.FloatField("balance")
    pics = models.ManyToManyField("Pic", verbose_name="pics", blank=True, null=True)
    created = models.DateTimeField("创建时间", auto_now_add=True)
    class Meta:
#         unique_together = (("brand", "province"),)
        verbose_name = "PlantInfo"
        verbose_name_plural = "PlantInfo MAG"
        
        
class FarmInfo(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField("name", max_length=64)
    area = models.FloatField("area")
    addr = models.CharField("addr", max_length=128, blank=True, null=True)
    desc = models.CharField("描述", max_length=200, blank=True, null=True)
    disa_weed = models.FloatField("disa_weed")
    disa_bug = models.FloatField("disa_bug")
    disa_dry = models.FloatField("disa_dry")
    position_x = models.FloatField("x")
    position_y = models.FloatField("y")
    pics = models.ManyToManyField("Pic", verbose_name="pics", blank=True, null=True)
    plant = models.ForeignKey("PlantInfo", verbose_name="plant", blank=True, null=True)
    owner = models.ForeignKey("UserInfo", verbose_name="owner", blank=True, null=True)
    class Meta:
#         unique_together = (("brand", "province"),)
        verbose_name = "FarmInfo"
        verbose_name_plural = "FarmInfo MAG"
        
        
class TimelineInfo(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    plantrecord = models.ForeignKey("PlantRecord", verbose_name="PlantRecord id")
    pic = models.CharField("pic", max_length=256, blank=True, null=True)
    admire = models.IntegerField("admire", default=0)
    date = models.DateTimeField("date")
    poster = models.ForeignKey("UserInfo", verbose_name="poster_id", blank=True, null=True)
    appendix = models.CharField("appendix", max_length=200)
    comments = models.ManyToManyField("Comment", verbose_name="Comments", blank=True, null=True)
    created = models.DateTimeField("创建时间", auto_now_add=True)
    class Meta:
#         unique_together = (("brand", "province"),)
        verbose_name = "TimelineInfo"
        verbose_name_plural = "TimelineInfo MAG"

class PlantRecord(models.Model):
    """种植记录
    """
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    farm = models.ForeignKey("FarmInfo", verbose_name="FarmInfo id")
    plant = models.ForeignKey("PlantInfo", verbose_name="PlantInfo id")
    begin = models.DateField('date')
    end = models.DateField('date', blank=True, null=True)
    finished = models.BooleanField('finished', default=False)
    created = models.DateTimeField("创建时间", auto_now_add=True)
    
    class Meta:
#         unique_together = (("brand", "province"),)
        verbose_name = "PlantRecord"
        verbose_name_plural = "PlantRecord MAG"


class Havest(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    plantrecord = models.ForeignKey("PlantRecord", verbose_name="PlantRecord id")
    latest = models.FloatField("latest")
    remain = models.FloatField("remain")
    date = models.DateField('date')
    update_date = models.DateField('update_date')
    attachment = models.CharField("attachment", max_length=200, blank=True, null=True)
    created = models.DateTimeField("创建时间", auto_now_add=True)
    
    class Meta:
#         unique_together = (("brand", "province"),)
        verbose_name = "Havest"
        verbose_name_plural = "Havest MAG"
        
        
class Comment(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey("UserInfo", verbose_name="uid", blank=True, null=True)
    desc = models.CharField("desc", max_length=200)
    class Meta:
#         unique_together = (("brand", "province"),)
        verbose_name = "Comment"
        verbose_name_plural = "Comment MAG"
        
class Pic(models.Model):
#     PIC_CHOICES = (
#                  ('portrait', u'头像'),
#                  ('plant', u'作物'),
#                  ('farm', u'农场'),
#                  ('timeline', u'timeline')
#                  )
#     type = models.CharField("type", choices=PIC_CHOICES, max_length=32)
    url = models.CharField("url", max_length=128, blank=True, null=True)
    file = models.FileField("图像", upload_to='.', help_text='')
    created = models.DateTimeField("创建时间", auto_now_add=True)
    class Meta:
#         unique_together = (("brand", "province"),)
        verbose_name = "Pic"
        verbose_name_plural = "Pic MAG"

