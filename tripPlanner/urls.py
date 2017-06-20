from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^logout/$', views.logoutPage, name='logoutPage'),
    url(r'^create-group/$', views.createGroup, name='createGroup'),
    url(r'^group/(?P<pk>\d+)/$', views.groupDetail, name='groupDetail'),
    url(r'^group/(?P<projpk>\d+)/invite/$',
        views.inviteFriend, name='inviteFriend'),
    url(r'^group/(?P<projpk>\d+)/invite/err(?P<errNo>\d)/(?P<username>\w+)/$',
        views.inviteResultFalse, name='inviteResultFalse'),
    url(r'^group/(?P<projpk>\d+)/invite/(?P<username>\w+)/$',
        views.inviteResultTrue, name='inviteResultTrue'),
]
