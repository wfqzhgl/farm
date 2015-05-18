from django.contrib import admin
from models import *


class UserInfoAdmin(admin.ModelAdmin):
    pass

admin.site.register(UserInfo, UserInfoAdmin)

class OperationInfoAdmin(admin.ModelAdmin):
    pass

admin.site.register(OperationInfo, OperationInfoAdmin)

class PlantInfoAdmin(admin.ModelAdmin):
    pass

admin.site.register(PlantInfo, PlantInfoAdmin)

class FarmInfoAdmin(admin.ModelAdmin):
    pass

admin.site.register(FarmInfo, FarmInfoAdmin)


class TimelineInfoAdmin(admin.ModelAdmin):
    pass

admin.site.register(TimelineInfo, TimelineInfoAdmin)


class CommentAdmin(admin.ModelAdmin):
    pass

admin.site.register(Comment, CommentAdmin)

class PicAdmin(admin.ModelAdmin):
    pass

admin.site.register(Pic, PicAdmin)

class PlantRecordAdmin(admin.ModelAdmin):
    pass
admin.site.register(PlantRecord, PlantRecordAdmin)

class ChargeCardAdmin(admin.ModelAdmin):
    pass
admin.site.register(ChargeCard, ChargeCardAdmin)

class ChargeHistoryAdmin(admin.ModelAdmin):
    pass
admin.site.register(ChargeHistory, ChargeHistoryAdmin)

