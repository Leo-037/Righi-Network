from django.conf.urls import url

from .views import *

urlpatterns = [
	url(r'^$', times_view),
	url(r'^(?P<slug>[0-9-]+)/$', issue_view),
	url(r'^[0-9-]+/articolo/(?P<slug>[\w-]+)/$', articolo_view),
	url(r'^aggiungi_numero/$', aggiungi_issue_view),
	url(r'(?P<slug>[0-9-]+)/aggiungi_articolo/$', aggiungi_articolo_view),
	url(r'^(?P<slug>[0-9-]+)/update/$', update_issue_view),
	url(r'^[0-9-]+/articolo/(?P<slug>[\w-]+)/update/$', update_articolo_view),
	url(r'^(?P<slug>[0-9-]+)/delete/$', delete_issue_view),
	url(r'^[0-9-]+/articolo/(?P<slug>[\w-]+)/delete/$', delete_articolo_view),
]
