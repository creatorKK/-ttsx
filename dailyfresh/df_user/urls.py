from django.conf.urls import url
from . import views
urlpatterns=[
    url(r'^index/$', views.index),
    url(r'^register/$', views.register),
    url(r'^register_handle/$', views.register_handle),
    url(r'^login/$', views.login),
    url('^login_handle/', views.login_handle),
    url('^$', views.center),
    url('^order/$', views.order),
    url('^site/$', views.site),
    url('^logout', views.logout)

]
