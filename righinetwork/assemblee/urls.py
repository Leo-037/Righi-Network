from django.conf.urls import url

from .views import *

urlpatterns = [
	url(r'^$', assemblee_view),
	url(r'^(?P<id_assemblea>[0-9]+)/$', dettagliassemblea_view),
	url(r'^[0-9]+/(?P<id_turno>[0-9]+)/$', dettagliturno_view),
	url(r'^aggiungi_assemblea/$', create_assemblea_view),
	url(r'^aggiungi_turno/(?P<id_assemblea>[0-9]+)/(?P<n_turni>[0-9]+)/$', create_turno_view),
	url(r'^aggiungi_gruppo/(?P<id_turno>[0-9]+)/$', create_gruppo_view),
	url(r'^(?P<id_assemblea>[0-9]+)/delete/$', delete_assemblea_view),
	url(r'^[0-9]+/(?P<id_turno>[0-9]+)/delete/$', delete_turno_view),
	url(r'^[0-9]+/[0-9]+/(?P<id_gruppo>[0-9]+)/delete/$', delete_gruppo_view),
	url(r'^(?P<id_assemblea>[0-9]+)/update/$', update_assemblea_view),
	url(r'^[0-9]+/(?P<id_turno>[0-9]+)/update/$', update_turno_view),
	url(r'^[0-9]+/[0-9]+/(?P<id_gruppo>[0-9]+)/update/$', update_gruppo_view),
	url(r'^[0-9]+/[0-9]+/(?P<id_gruppo>[0-9]+)/iscritti/$', iscritti_view),
	url(r'^(?P<id_assemblea>[0-9]+)/(?P<id_turno>[0-9]+)/(?P<id_gruppo>[0-9]+)/iscrizione/$', iscrizione_view,
	    name = 'iscriviti'),
	url(r'^(?P<id_assemblea>[0-9]+)/(?P<id_turno>[0-9]+)/(?P<id_gruppo>[0-9]+)/disiscrizione/$', disiscrizione_view,
	    name = 'disiscriviti'),
]
