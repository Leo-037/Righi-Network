from django.conf.urls import url

from .views import assemblee_view, create_assemblea_view, dettagliassemblea_view, dettagliturno_view, iscritti_view, \
	iscrizione_view, disiscrizione_view

urlpatterns = [
	url(r'^$', assemblee_view, name = 'assemblee'),
	url(r'^aggiungi/$', create_assemblea_view, name = 'aggiungi_assemblea'),
	url(r'^(?P<id_assemblea>[0-9]+)/$', dettagliassemblea_view, name = 'dettagliassemblea'),
	url(r'^[0-9]+/(?P<id_turno>[0-9]+)/$', dettagliturno_view, name = 'dettagliturno'),
	url(r'^[0-9]+/[0-9]+/(?P<id_gruppo>[0-9]+)/iscritti/$', iscritti_view, name = 'iscritti'),
	url(r'^(?P<id_assemblea>[0-9]+)/(?P<id_turno>[0-9]+)/(?P<id_gruppo>[0-9]+)/iscrizione/$', iscrizione_view, name = 'iscriviti'),
	url(r'^(?P<id_assemblea>[0-9]+)/(?P<id_turno>[0-9]+)/(?P<id_gruppo>[0-9]+)/disiscrizione/$', disiscrizione_view, name = 'disiscriviti'),

]
