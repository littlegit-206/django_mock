from django.urls import path

from . import views
from django.conf.urls import url
urlpatterns = [
   # url(r'^$', views.login, name='login'),
    url(r'login/', views.login, name='login'),
    url(r'^index/$', views.index, name='index'),
    url(r'^index1/$', views.index1, name='index1'),
    url(r'^idetail/(\w+)$', views.Interface_Table, name='Interface_Table'),
    url(r'^edit/$', views.edit, name='edit'),
    url(r'^edit/(\w+)$', views.edit, name='edit'),
    url(r'^record_add/$', views.record_add, name='record_add'),
    url(r'^delete/$', views.delete, name='delete'),
    url(r'^StopOrOpen/$', views.stopOrOpen, name='StopOrOpen'),
    url(r'^mock/$', views.mock, name='mock'),

]