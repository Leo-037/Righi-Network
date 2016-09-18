from django.conf.urls import url

from .views import *

urlpatterns = [
	url(r'^$', settimana_view, name = 'settimana'),
	url(r'^scegli_gruppo/(?P<id_turno>[0-9]+)/$', scegli_gruppo_view),
	url(r'^aggiungi/$', create_settimana_view),
	# url(r'^(?P<id_settimana>[0-9]+)/$', dettaglisettimana_view),
	# url(r'^[0-9]+/(?P<id_giorno>[0-9]+)/$', dettagligiorno_view),
	# url(r'^[0-9]+/[0-9]+/(?P<id_turno>[0-9]+)/$', dettagliturno_view),
	url(r'^[0-9]+/[0-9]+/[0-9]+/(?P<id_gruppo>[0-9]+)/iscritti/$', iscritti_view),
	url(r'^(?P<id_settimana>[0-9]+)/(?P<id_giorno>[0-9]+)/(?P<id_turno>[0-9]+)/(?P<id_gruppo>[0-9]+)/iscrizione/$', iscrizione_view),
	url(r'^(?P<id_settimana>[0-9]+)/(?P<id_giorno>[0-9]+)/(?P<id_turno>[0-9]+)/(?P<id_gruppo>[0-9]+)/disiscrizione/$', disiscrizione_view),

]
