from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from apps.auth_custom import *
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'farm.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^apps/', include('apps.urls', namespace='apps')),
    
    (r'^accounts/login/$', login_custom),
    (r'^accounts/logout/$', login_required(logout_custom)),
    (r'^accounts/password_change/$', login_required(password_change)),
    (r'^$', login_custom),
)
