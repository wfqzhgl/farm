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
                        url(r'^change_psw[/]?$', "change_psw", name='change_psw'),
                        
                        url(r'^rdm_cus[/]?$', "rdm_user_info", name='rdm_user_info'),
                        url(r'^time_line[/]?$', "get_time_line", name='get_time_line'),
                        url(r'^pic_praise[/]?$', "pic_praise", name='pic_praise'),
                        
                        url(r'^farm_info[/]?$', "get_farm_info", name='get_farm_info'),
                        url(r'^farm_list[/]?$', "get_farm_list", name='get_farm_list'),
                        
                        url(r'^user_info[/]?$', "get_user_info", name='get_user_info'),
                        url(r'^modify[/]?$', "modify_user_info", name='modify_user_info'),
                        url(r'^buddy_follow[/]?$', "buddy_follow", name='buddy_follow'),
                        url(r'^customer_buddy_list[/]?$', "get_buddy_list", name='get_buddy_list'),
                        
                        url(r'^free_farm_list[/]?$', "get_free_farm_list", name='get_free_farm_list'),
                        url(r'^plant_for_farm[/]?$', "get_plant_for_farm", name='get_plant_for_farm'),
                        
                        url(r'^recharge[/]?$', "recharge", name='recharge'),
                        url(r'^apply[/]?$', "apply_for_farm", name='apply_for_farm'),
                        url(r'^consum_history[/]?$', "get_op_history", name='get_op_history'),
                        url(r'^rent[/]?$', "rent_for_farm", name='rent_for_farm'),
                        url(r'^unrent[/]?$', "unrent_for_farm", name='unrent_for_farm'),
                        
                        url(r'^pic_commens_edit[/]?$', "edit_comment", name='edit_comment'),
                        url(r'^pic_commens_get[/]?$', "get_comments_of_timeline", name='get_comments_of_timeline'),
                        
                       )
