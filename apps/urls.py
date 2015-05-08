# -*-coding:utf8-*-

from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from views import *

urlpatterns = patterns('apps.views',
#                        url(r'^index[/]?$', login_required(PatientView.as_view()), name='list_patient'),
#                        url(r'^addhis/(?P<uid>\d+)[/]?$',login_required(BHistoryCreate.as_view()),name='add_bhistory'),
                       
                        url(r'^register[/]?$', "reg", name='reg'),
                        url(r'^login[/]?$', "login", name='login'),
                        url(r'^upload[/]?$', "upload", name='upload'),
                        
                        url(r'^logout[/]?$', "logout", name='logout'),
                        url(r'^rdm_cus[/]?$', "rdm_user_info", name='rdm_user_info'),
                        url(r'^time_line[/]?$', "get_time_line", name='get_time_line'),
                        url(r'^farm_list[/]?$', "get_farm_list", name='get_farm_list'),
                        
                        
                        
                       )
