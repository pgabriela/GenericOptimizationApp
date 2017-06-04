from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^logout/', views.logoutPage, name='logoutPage'),
    url(r'^create-group/', views.createGroup, name='createGroup'),
]
