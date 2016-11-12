from django.conf.urls import url

from .views import *

urlpatterns = [
	url(r'^$', bilancio_chart_view),
	url(r'^aggiorna/$', aggiorna_bilancio_view),
	url(r'^(?P<id_bilancio>[0-9]+)/update/$', update_bilancio_view),
	url(r'^(?P<id_bilancio>[0-9]+)/delete/$', delete_bilancio_view),
]
