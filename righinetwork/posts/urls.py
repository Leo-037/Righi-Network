from django.conf.urls import url
from django.contrib import admin

from .views import (
	post_list,
	post_create,
	post_detail,
	post_update,
	post_delete,
	redirect,
	)

urlpatterns = [
	url(r'^$', post_list, name='list'),
	url(r'^posts/$', redirect),
    url(r'^posts/create/$', post_create),
    url(r'^posts/(?P<slug>[\w-]+)/$', post_detail, name='detail'),
    url(r'^posts/(?P<slug>[\w-]+)/edit/$', post_update, name='update'),
    url(r'^posts/(?P<slug>[\w-]+)/delete/$', post_delete),
]
