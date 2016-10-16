from django.conf.urls import url

from .views import *

urlpatterns = [
	url(r'^$', settimana_view, name = 'settimana'),
	# url(r'^update/$', update_settimana_view, name = 'settimana'),
	url(r'^(?P<id_giorno>[0-9]+)/$', dettagligiorno_view),
	url(r'^scegli_gruppo/(?P<id_turno>[0-9]+)/$', dettagliturno_view),
	url(r'^aggiungi_settimana/$', create_settimana_view),
	url(r'^aggiungi_turno/(?P<id_giorno>[0-9]+)/$', create_turno_view),
	url(r'^aggiungi_gruppo/(?P<id_turno>[0-9]+)/$', create_gruppo_view),
	url(r'^scegli_gruppo/(?P<id_turno>[0-9]+)/update/$', update_turno_view),
	url(r'^scegli_gruppo/[0-9]+/(?P<id_gruppo>[0-9]+)/update/$', update_gruppo_view),
	url(r'^scegli_gruppo/(?P<id_turno>[0-9]+)/delete/$', delete_turno_view),
	url(r'^scegli_gruppo/[0-9]+/(?P<id_gruppo>[0-9]+)/delete/$', delete_gruppo_view),
	url(r'^(?P<id_settimana>[0-9]+)/delete/$', delete_settimana_view),
	url(r'^[0-9]+/[0-9]+/[0-9]+/(?P<id_gruppo>[0-9]+)/iscritti/$', iscritti_view),
	url(r'^(?P<id_settimana>[0-9]+)/(?P<id_giorno>[0-9]+)/(?P<id_turno>[0-9]+)/(?P<id_gruppo>[0-9]+)/iscrizione/$', iscrizione_view),
	url(r'^(?P<id_settimana>[0-9]+)/(?P<id_giorno>[0-9]+)/(?P<id_turno>[0-9]+)/(?P<id_gruppo>[0-9]+)/disiscrizione/$', disiscrizione_view),
]
