from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^createnode/(?P<id>\d+)$', views.createnode, name='createnode'),
    url(r'^createstory$', views.createstory, name='createstory'),
    url(r'^node/(?P<id>\d+)$', views.node, name='node'),
    url(r'^nodelist/(?P<parentid>\d+)/(?P<id>\d+)?$', views.nodelist, name='nodelist'),
]
