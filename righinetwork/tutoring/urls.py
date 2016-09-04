from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

from .views import list_tutors, tutor_form_view, richiedi_tutor, approva_tutor, elimina_tutor

urlpatterns = [
	url(r'^$', list_tutors),
	url(r'^richiedi-tutoring/(?P<id_tutor>[1-9]+)$', richiedi_tutor),
	url(r'^elimina-tutor/(?P<id_tutor>[1-9]+)$', elimina_tutor),
	url(r'^diventa-tutor/$', tutor_form_view),
	url(r'^approva-tutoring/(?P<id_tutor>[1-9]+)$', approva_tutor),
 ]

